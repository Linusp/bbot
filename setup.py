#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


VERSION = '0.2.0'

setup(
    name='bearybot',
    version=VERSION,
    url='https://github.com/Linusp/bbot',
    author='Linusp',
    description='A simple bot for BearcyChat',
    license='BSD',
    packages=find_packages(),
    scripts=['bin/bbot'],
    install_requires=[
        'Flask>=0.10.1,<1.0.0',
        'requests>=2.7.0,<3.0.0',
        'giphypop>=0.2,<1.0',
        'wikipedia==1.4.0,<2.0.0',
    ],
    include_package_data=True,
    zip_safe=False,
)
