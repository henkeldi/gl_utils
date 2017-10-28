# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = ''
with open('gl_utils/version.py', 'r') as f:
	version = f.read().split('=')[1]

setup(
    name='gl_utils',
    version=version,
    description='Helper functions for PyOpenGL 4.5',
    author='Dimitri Henkel',
    author_email='Dimitri.Henkel@gmail.com',
    packages=find_packages(exclude=('test', 'doc'))
)