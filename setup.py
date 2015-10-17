#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pip.req import parse_requirements


VERSION = '20151017'

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='bearybot',
    version=VERSION,
    url='https://github.com/Linusp/bbot',
    author='Linusp',
    description='A simple bot for BearcyChat',
    license='BSD',
    packages=find_packages(),
    scripts=['bin/bbot'],
    install_requires=reqs,
    include_package_data=True,
    zip_safe=False,
)
