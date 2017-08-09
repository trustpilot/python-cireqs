
[![Build Status](https://travis-ci.org/trustpilot/python-cireqs.svg?branch=master)](https://travis-ci.org/trustpilot/python-cireqs) [![Latest Version](https://img.shields.io/pypi/v/cireqs.svg)](https://pypi.python.org/pypi/cireqs) [![Python Support](https://img.shields.io/pypi/pyversions/cireqs.svg)](https://pypi.python.org/pypi/cireqs)

# cireqs

Tool to expand and pin requirements files and verify that they are complete.

## install
Install from pypi.

`pip install cireqs`

## usage

Cireqs uses overridable defaults:

* **dirpath:** set to PWD
* **pythonversion:** set to `3.5.2`
* **output_requirements_filename:** set to `requirements.txt`
* **input_requirements_filename:** set to:
* * `requirements.txt` in `verify_requirements`
* * `requirements_to_expand.txt` in `expand_requirements`


```bash
cireqs --dirpath /tmp expand_requirements input_requirements_filename output_requirements_filename

cireqs verify_requirements input_requirements
```

Use it in your **CI** of choice!!!

**travis**
```yaml
services:
  - docker

before_script:
  - pip install cireqs

script:
  - cireqs verify_requirements
```

