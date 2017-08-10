__version__ = '0.0.3'
import logging
import os
from subprocess import check_output, CalledProcessError, TimeoutExpired, STDOUT, DEVNULL


logger = logging.getLogger(__name__)


def set_log_level(level):
    logger.setLevel(level)


def docker_kill_and_remove(ctr_name):
    for action in ('kill', 'rm'):
        try:
            check_output(['docker', action, ctr_name], stderr=STDOUT)
        except Exception as exc:
            logger.exception('could not stop docker container')


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
       'docker', 'run', '--rm', '--name', ctr_name, *volumes, *working_dir,
       docker_image, 'sh', '-c', command
    ]
    logger.debug("issuing command: %s", " ".join(full_command_list))
    try:

        output = check_output(
            full_command_list,
            timeout=timeout,
            stderr=STDOUT
        )
        return output
    except Exception as exc:
        if isinstance(exc, CalledProcessError):
            logger.exception("command resulted in error. " + ' '.join(full_command_list))
        elif isinstance(exc, TimeoutExpired):
            logger.warning("received timeout")
        docker_kill_and_remove(ctr_name)
        exit(1)


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
    frozen_reqs = docker_execute(commands, volumes, working_dir, **kwargs).decode('utf-8')

    frozen_token = "## The following requirements were added by pip freeze:\n"

    t = frozen_reqs.rfind(frozen_token)

    new_requirements = [req for req in frozen_reqs[t+len(frozen_token):].split('\n') if req]

    if new_requirements:
        logger.error("new requirements found: {}".format(
            ' '.join(new_requirements)))
        exit(1)
    logger.debug("Requirements are up to date")
