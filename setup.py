#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os.path

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

readme = read_md('README.md')

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click==6.7',
    'click-log==0.1.8',
]

test_requirements = [
    'pytest==3.2.0',
    'prospector==0.12.7',
    'pylint==1.9.2',
    'isort==4.2.15' # dependency of pylint'pytest==3.2.0'
]

extras = {
    'test': test_requirements + requirements
}

# get version
metadata = {}
version_filename = os.path.join(os.path.dirname(__file__), 'cireqs','__version__.py')
exec(open(version_filename).read(), None, metadata)

setup(
    name='cireqs',
    version=metadata['__version__'],
    description="cli tool to verify and update requirements files",
    long_description=readme + '\n\n' + history,
    author="jgv",
    author_email='jgv@trustpilot.com',
    url='https://github.com/trustpilot/python-cireqs',
    packages=[
        'cireqs',
    ],
    package_dir={'cireqs':
                 'cireqs'},
    entry_points={
        'console_scripts': [
            'cireqs=cireqs.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='cireqs requirements ci',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    extras_require=extras,

)
