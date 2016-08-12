#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    setup.py
    ------------------------------------------------------------

    A setup tool for installing espider to your computer.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'


from distutils.core import setup

setup(name='espider',
      version='0.1.2',
      description='A simply constructed web crawling and web scraping framework that is easy to install and use',
      author='MeteorKepler',
      author_email='JimRanor@outlook.com',
      packages=['espider', 'espider.tools'],
    )