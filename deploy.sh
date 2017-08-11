#!/usr/bin/python
import importlib
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_sudo():
    return  os.getuid() == 0


def import_yaml():

    try:
        importlib.import_module('yaml')
    except ImportError:
        import pip
        pip.main(['install', 'pyyaml'])
    return importlib.import_module('yaml')


def get_config():
    yaml = import_yaml()
    try:
        travis_config = open('.travis.yml', 'r')
    except:
        travis_config = open('.travis.yaml', 'r')
    travis_config = yaml.load(travis_config)
    return travis_config['deploy']


def main():
    if not is_sudo():
        exit("Not sudo")
    config = get_config()
    print(config)
    print("gonna be: " + config["how-silly"])
    print(os.environ['lolcat'])


if __name__ == "__main__":
    main()