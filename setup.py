#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

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
    'prospector==0.12.7'
]

extras = {
    'test': test_requirements + requirements,
}

setup(
    name='cireqs',
    version='0.0.4',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    extras_require=extras,

)
