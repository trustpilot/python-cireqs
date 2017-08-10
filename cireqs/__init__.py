__version__ = '0.0.4'


import logging
import os
import difflib
from subprocess import check_output, CalledProcessError, STDOUT
try:
    from subprocess import TimeoutExpired, DEVNULL
except ImportError:
    TimeoutExpired = None
    DEVNULL = STDOUT


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


def docker_execute(commands, volumes=None, working_dir=None, python_version='3.5.2', timeout=10, **kwargs):
    volumes = volumes or {}
    volumes = [t for k,v in volumes.items() for t in ['-v', ':'.join([k,v])]]
    working_dir = ['-w', working_dir] if working_dir else []
    command = ' && '.join(commands)
    ctr_name = 'cireqs_container'
    docker_image = 'python:{}'.format(python_version)

    # check if has image locally:
    has_image = check_output(
        ['docker', 'images','-q', docker_image],
        stderr=DEVNULL
    )
    if not has_image:
        logger.debug('pulling docker image: {}'.format(docker_image))
        check_output(
            ['docker', 'pull', docker_image],
            stderr=STDOUT
        )

    full_command_list = [
       'docker', 'run', '--rm', '--name', ctr_name] + volumes + working_dir + [
       docker_image, 'sh', '-c', command
    ]
    logger.debug("issuing command: %s", " ".join(full_command_list))
    timeout_kwargs = {'timeout':timeout} if TimeoutExpired is not None else {}
    try:
        output = check_output(
            full_command_list,
            stderr=STDOUT,
            **timeout_kwargs
        )
        return output
    except Exception as exc:
        if isinstance(exc, CalledProcessError):
            logger.exception("Command resulted in error. " + ' '.join(full_command_list))
        elif isinstance(exc, TimeoutExpired):
            logger.warning("received timeout")
        docker_kill_and_remove(ctr_name)
        exit(-1)


def expand_requirements(dir_path, requirements_filename, expanded_requirements_filename, **kwargs):
    commands = [
        "pip install -q -r {}".format(requirements_filename),
        "pip freeze -r {} > {}".format(
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
        "pip install -q -r {} ".format(requirements_filename),
        "pip freeze -r {} ".format(requirements_filename)
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
