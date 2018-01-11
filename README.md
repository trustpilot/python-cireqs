
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
* **pythonversion:** set to `3.5.2`
* **output_requirements_filename:** set to `requirements.txt`
* **input_requirements_filename:** set to:
* * `requirements.txt` in *verify*
* * `requirements_to_expand.txt` in *expand*

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
  --pythonversion TEXT  python version to use for calculating dependencies
  --dirpath TEXT        path to directory containing requirement files,
                        defaults to PWD
  -v, --verbosity LVL   Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help                Show this message and exit.

Commands:
  expand  Expand given requirements file by extending...
  verify  Verifying that given requirements file is not...
```
