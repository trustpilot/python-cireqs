
[![Build Status](https://travis-ci.org/trustpilot/python-cireqs.svg?branch=master)](https://travis-ci.org/trustpilot/python-cireqs) [![Latest Version](https://img.shields.io/pypi/v/cireqs.svg)](https://pypi.python.org/pypi/cireqs) [![Python Support](https://img.shields.io/pypi/pyversions/cireqs.svg)](https://pypi.python.org/pypi/cireqs)

# cireqs

Tool to expand and pin requirements files and verify that they are complete.

## Installation

Install from [pypi](https://pypi.python.org/pypi/cireqs).

`pip install cireqs`

Cireqs needs a working install of docker locally.

## Usage

Use cireqs to expand and pin down your dependencies.

You can then check in the resulting requirements file and stop worrying about floating versions.

```bash
cireqs --dirpath /tmp expand input_requirements_filename output_requirements_filename
```

Use cireqs to verify that a requirements file is pinned down and includes all requirements of requirements.
```bash
cireqs verify input_requirements
```

#### Defaults

Cireqs uses overridable defaults:

* **dirpath:** set to current working directory (`PWD`)
* **pythonversion:** set to `3.6.1`
* **output_requirements_filename:** set to `requirements.txt`
* **input_requirements_filename:** set to:
* * `requirements.txt` in *verify*
* * `requirements_to_expand.txt` in *expand*

## private packages

To install private packages like with Gemfury you have to inject your private access token as an env var to cireqs, use the **--envar** (`-e`) option to pass in env-vars to the pip install process. you can specify them in the following ways:

```
cireqs --envar foo=bar
```
Will set the envvar foo to the value bar

```
cireqs --envvar foo
```
will set the envvar foo to the value of the hosts `foo` env var.

### Gemfury example

create a requirements_to_expand.txt file with the following contents:
```
--index-url https://${GEM_FURY_TOKEN}@pypi.fury.io/trustpilot/
--extra-index-url https://pypi.org/simple/
secret_private_package
```
to expand run
```
cireqs --envvar GEM_FURY_TOKEN expand
```
And cireqs will inject the hosts value of `GEM_FURY_TOKEN` into the `expand` process.

## Continuous Integration

Use it in your **CI** of choice!!!

**travis**
```yaml
services:
  - docker

before_script:
  - pip install cireqs

script:
  - cireqs verify
```

## CLI

Cireqs includes the `cireqs` command:

```
Usage: cireqs [OPTIONS] COMMAND [ARGS]...

Options:
  --pythonversion TEXT  python version to use for calculating dependencies,
                        defaults to 3.6.1
  --dirpath TEXT        path to directory containing requirement files,
                        defaults to PWD
  --timeout INTEGER     how long to wait for docker commands, defaults to 120s
  -e, --envvar TEXT     environment var ENV_VAR=VALUE (or ENV_VAR to copy
                        env_var), multiple allowed, defaults to None
  -V, --version         show version and exit
  --dry                 print out docker command line without running it
  -v, --verbosity LVL   Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help                Show this message and exit.

Commands:
  expand               Expand given requirements file by extending...
  expand_requirements
  verify               Verifying that given requirements file is not...
  verify_requirements
```
