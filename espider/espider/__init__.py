#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.*
    ------------------------------------------------------------

    Package espider is a simply constructed web crawling and scrabing framework that is easy to use. 
    This package includes modules mentioned below:

    |name           |description                                                                 |
    |:-------------:|:---------------------------------------------------------------------------|
    |spider         |Scribe web sources automatically and save original sources                  |
    |parser         |Parse the sources that are scribed by spider                                |
    |httphandler    |Manipulate module that communicate with web server                          |
    |proxy          |A proxy handler provides Internet connection                                |
    |selephan       |Use selenium and phantomjs to load website instantly just like a browser do |
    |mysql          |Provide mysql service while saving data                                     |
    |log            |Support configurable console and file logging                               |
    |util           |Including some useful functions the project need                            |
    |config         |Loading configuration from both config_default and config_override          |
    |config_default |Define default settings. You should always change configs in config_override|

    You can refer to README.md for further instruction.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'
__version__ = '0.1.1'