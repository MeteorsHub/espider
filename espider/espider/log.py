#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    espider.log
    -----------------------------------------------------------

    Define logging used in espider including console and file logging.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import os
import logging

from espider.config import configs

__all__ = [
    'Logger',
    ]

# Diffrent log formater, you can change this in configs
formatter = ['%(asctime)s %(module)s %(levelname)s %(message)s',
             '%(levelname)s %(message)s',
             '%(asctime)s %(pathname)s %(module)s %(levelname)s %(message)s'
             ]

logging.basicConfig(level=configs.logging.level,
                    format=formatter[configs.logging.formatter_style])

Logger = logging.getLogger('')

if configs.logging.filelog:
    path, file = os.path.split(configs.logging.filename)
    if not os.path.exists(path):
        os.makedirs(path)
    filelog = logging.FileHandler(configs.logging.filename, configs.logging.filemode)
    filelog.setFormatter(logging.Formatter(formatter[int(configs.logging.formatter_style)]))
    filelog.setLevel(configs.logging.level)

    Logger.addHandler(filelog)

if __name__ == '__main__':
    Logger.debug('This is a debug message')
    Logger.info('This is an info message')
    Logger.warning('This is a warning message')
    Logger.error('This is an errer message')
    Logger.critical('This is a critical message')
