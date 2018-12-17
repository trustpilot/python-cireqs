History
=======

0.0.1 (2017-08-09)
------------------

* git init


0.0.2 (2017-08-09)
------------------

* missing manifest file

0.0.3 (2017-08-10)
------------------

* readme changes
* cli splash changes
* make cireqs functions pass python version to docker_execute
* pass timeout param from cli to cireqs

0.0.4 (2017-08-10)
------------------

* tox testing for py27, py33, py34, py35, py36
* more thorough diffing of requirements files
* more tests
* use prospector for linting

0.1.3 (2017-08-11)
------------------

* single source version in setup.py and cli

0.2.2 (2017-08-14)
------------------

* default timeout value for docker operations increased to 120 seconds (from 10)

1.0.0 (2017-11-01)
------------------

* introduce verify and expand and deprecate verify_requirements and expand_requirements by showing warnings
* message when commands are successful

1.0.3 (2018-03-26)
------------------

* Handle pip giving an upgrade warning

1.0.4 (2018-07-24)
------------------

* Upgrade pip before installing requirements to avoid upgrade error.

2.0.0 (2018-12-14)
------------------

* added --dry option for running dry (printing docker cmd line)
* added -V for printing version
* added --envvar (-e) for injecting env vars into the docker container running pip install, useful for private repos like in Gemfury.io

2.0.1 (2018-12-14)
------------------

* warns and exits on missing input_requirements file

2.0.2 (2018-12-14)
------------------

* warns and exits on package requiring different pythonversion than specified

2.0.3 (2018-12-17)
------------------

* avoid using alpine linux as bse image since its compiled without gcc (makes it impossible to install UVLOOP for instance)