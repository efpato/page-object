#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='page-object',
    version='2.0.0',
    url='https://github.com/efpato/page-object',
    author='Sergey Demenok',
    author_email='sergey.demenok@gmail.com',
    description='Page Objects for Python',
    packages=[
        'page_object',
        'page_object.ui',
        'page_object.ui.jquery'
    ]
)
