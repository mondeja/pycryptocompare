#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = 'pycryptocompare',
    version = '0.0.1',
    url = 'https://github.com/mondeja/pycryptocompare',
    download_url = 'https://github.com/mondeja/pycryptocompare/archive/master.zip',
    author = 'Álvaro Mondéjar <mondejar1994@gmail.com>',
    author_email = 'mondejar1994@gmail.com',
    license = 'BSD License',
    packages = ['pycryptocompare'],
    description = 'Python3 API Wrapper for CryptoCompare',
    long_description = open('README.md','r').read(),
    keywords = ['Cryptocompare', 'cryptocurrency', 'API', 'wrapper', 'CryptoExchanges'],
    install_requires = requirements
)
