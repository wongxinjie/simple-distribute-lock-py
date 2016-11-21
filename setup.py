#!/usr/bin/env python
from setuptools import setup

setup(
    name='distro-lock',
    version='1.0',
    description='A simple distribute lock base on redis setnx',
    author='wongxinjie',
    author_email='wongxinjierun@gmail.com',
    url='https://github.com/wongxinjie/distribute-lock-py',
    install_requires=[
        'redis>=2.10.0'
    ],
    py_modules=['distrolock'],
)
