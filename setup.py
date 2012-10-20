#!/usr/bin/env python
import os
import re
from setuptools import setup

__doc__="""
CouchDB interactive shell
"""

version = '0.0.1'

setup(name='couchli',
    version=version,
    description=__doc__,
    author='Gavin Wahl',
    author_email='gavinwahl@gmail.com',
    scripts=['couchli.py'],
    platforms = 'any',
    license='BSD',
    install_requires=['requests'],
)
