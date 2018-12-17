import logging
import os
import difflib
import time
from subprocess import check_output, CalledProcessError, STDOUT, Popen, PIPE

try:
    from subprocess import TimeoutExpired, DEVNULL
except ImportError:
    TimeoutExpired = None
    DEVNULL = STDOUT

class WrongPythonError(Exception):
    pass

logger = logging.getLogger(__name__)


def set_log_level(level):
    logger.setLevel(level)

def docker_kill_and_remove(ctr_name):
    try:
        try:
            is_running = check_output(['docker', 'top', ctr_name], stderr=DEVNULL)
        except:
            pass
        else:
            check_output(['docker', 'kill', ctr_name], stderr=STDOUT)
        try:
            has_image = check_output(['docker', 'images', '-q', ctr_name], stderr=DEVNULL)
            assert has_image
        except:
            pass
        else:
            check_output(['docker', 'rm', ctr_name], stderr=STDOUT)
    except:
        logger.error('could not stop docker container:{}'.format(ctr_name))


def docker_execute(commands, volumes=None, working_dir=None, env_vars=None, python_version='3.6.1', timeout=120, run_dry=False, **kwargs):
    volumes = volumes or {}
    volumes = [t for k,v in volumes.items() for t in ['-v', ':'.join([k,v])]]
    working_dir = ['-w', working_dir] if working_dir else []
    commands = ['/usr/local/bin/pip install --upgrade -q pip && /usr/local/bin/pip install --upgrade -q setuptools'] + commands
    command =  ' && '.join(commands)
    env_vars = [e for env_var in env_vars for e in ['-e', env_var]] if env_vars else []

    ctr_name = 'cireqs_container'
    docker_image = 'python:{}'.format(python_version)

    # check if has image locally:
    has_image = check_output(
        ['docker', 'images','-q', docker_image],
        stderr=DEVNULL
    )
    if not has_image:
        logger.debug('pulling docker image: {}'.format(docker_image))
        try:
            check_output(
                ['docker', 'pull', docker_image],
                stderr=STDOUT
            )
        except Exception as exc:
            if isinstance(exc, CalledProcessError):
                logger.error("Couldn't pull image:{}, does it exist?".format(docker_image))
            else:
                logger.error("UNKNOWN ERROR\n" + str(exc))
            exit(-1)

    full_command_list = [
       'docker', 'run', '--rm', '--name', ctr_name] + env_vars + volumes + working_dir + [
       docker_image, 'sh', '-c', command
    ]
    if run_dry:
        print(' '.join(full_command_list))
        exit(0)

    logger.debug("issuing command: %s", " ".join(full_command_list))
    timeout_kwargs = {'timeout':timeout} if TimeoutExpired is not None else {}
    try:

        p = Popen(full_command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = err = None
        for t in range(timeout):
            time.sleep(1)
            if p.poll() is not None:
                output, err = p.communicate()
                rc = p.returncode
                break
        p.kill()
        if rc is None:
            raise TimeoutExpired()
        if rc != 0:
            output = output.decode('ascii')
            err = err.decode('ascii')

            if 'requires Python ' in output:
                required_python_version = output.split('requires Python ')[1].split(' ')[0][:-3]
                package = output.strip().rsplit('RuntimeError: ', 1)[1].strip().split(' ', 1)[0]
                raise WrongPythonError("wrong python version, '{1}' requires:{0}, try setting --pythonversion to {0}".format(required_python_version, package))

            raise Exception(output + err)
        return output
    except Exception as exc:
        if isinstance(exc, CalledProcessError):
            logger.error("Command resulted in error. " + ' '.join(full_command_list))
        elif isinstance(exc, TimeoutExpired):
            logger.warning("received timeout")
        elif isinstance(exc, WrongPythonError):
            logger.error(exc)
        else:
            logger.error("UNKNOWN ERROR\n" + str(exc))
        docker_kill_and_remove(ctr_name)
        exit(-1)


def expand_requirements(dir_path, requirements_filename, expanded_requirements_filename, **kwargs):
    commands = [
        "/usr/local/bin/pip install -r {}".format(requirements_filename),
        "/usr/local/bin/pip freeze -r {} > {}".format(
            requirements_filename, expanded_requirements_filename
        )
    ]
    dir_path = os.path.normpath(dir_path) + os.sep
    working_dir = '/src'
    volumes = {
        dir_path: '/src'
    }
    docker_execute(commands, volumes, working_dir, **kwargs)
    logger.debug("Requirements expanded from {} to {}".format(
        requirements_filename, expanded_requirements_filename))


def check_if_requirements_are_up_to_date(dir_path, requirements_filename, **kwargs):
    commands = [
        "/usr/local/bin/pip install -q -r {} ".format(requirements_filename),
        "/usr/local/bin/pip freeze -q -r {} ".format(requirements_filename)
    ]
    dir_path = os.path.normpath(dir_path) + os.sep
    working_dir = '/src'
    volumes = {
        dir_path: '/src'
    }
    frozen_reqs = docker_execute(commands, volumes, working_dir, **kwargs).decode('utf-8').strip().splitlines()
    added = []
    removed = []
    with open(os.path.join(dir_path, requirements_filename), 'r') as requirements_file:
        diff_set = difflib.unified_diff(
            requirements_file.read().strip().splitlines(),
            frozen_reqs,
            fromfile='input',
            tofile='output',
            n=0,
        )
        for line in diff_set:
            for prefix in ('---', '+++', '@@', '+##', '-##'):
                if line.startswith(prefix):
                    break
            else:
                prefix, diff = line[0], line[1:]
                if prefix == '+':
                    added.append(diff)
                else:
                    removed.append(diff)
    if added or removed:
        logger.error("Requirements not up to date! added: '{}', removed: '{}'".format(
            ', '.join(added), ', '.join(removed)))
        exit(-1)
