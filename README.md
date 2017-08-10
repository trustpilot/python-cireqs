
[![Build Status](https://travis-ci.org/trustpilot/python-cireqs.svg?branch=master)](https://travis-ci.org/trustpilot/python-cireqs) [![Latest Version](https://img.shields.io/pypi/v/cireqs.svg)](https://pypi.python.org/pypi/cireqs) [![Python Support](https://img.shields.io/pypi/pyversions/cireqs.svg)](https://pypi.python.org/pypi/cireqs)

# cireqs

Tool to expand and pin requirements files and verify that they are complete.

## install
Install from pypi.

`pip install cireqs`

Cireqs needs a working install of docker locally.

## usage

Use cireqs to expand and pin down your dependencies.

You can then check in the resulting requirements file and stop worrying about floating versions.

```bash
cireqs --dirpath /tmp expand_requirements input_requirements_filename output_requirements_filename
```

Use cireqs to verify that a requirements file is pinned down and includes all requirements of requirements.
```bash
cireqs verify_requirements input_requirements
```

#### defaults

Cireqs uses overridable defaults:

* **dirpath:** set to current working directory (`PWD`)
* **pythonversion:** set to `3.5.2`
* **output_requirements_filename:** set to `requirements.txt`
* **input_requirements_filename:** set to:
* * `requirements.txt` in *verify_requirements*
* * `requirements_to_expand.txt` in *expand_requirements*

## continous integration
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


## cli
Cireqs includes the `cireqs` command:

```
           o8o
           `"'
 .ooooo.  oooo  oooo d8b  .ooooo.   .ooooo oo  .oooo.o
d88' `"Y8 `888  `888""8P d88' `88b d88' `888  d88(  "8
888        888   888     888ooo888 888   888  `"Y88b.
888   .o8  888   888     888    .o 888   888  o.  )88b
`Y8bod8P' o888o d888b    `Y8bod8P' `V8bod888  8""888P'
                                         888.
                                         8P'  v0.0.3

Usage: cireqs [OPTIONS] COMMAND [ARGS]...

Options:
  --pythonversion TEXT  python version to use for calculating dependencies
  --dirpath TEXT        path to directory containing requirement files,
                        defaults to PWD
  -v, --verbosity LVL   Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help                Show this message and exit.

Commands:
  expand_requirements  Expand given requirements file by extending...
  verify_requirements  verifying that given requirements file is not...
```
