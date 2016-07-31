#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    espider.log
    -----------------------------------------------------------

    Define logging used in espider

"""

__author__ = 'MeterKepler'

import logging
import os

from espider import config

# diffrent log formater
formatter = ['%(asctime)s %(module)s %(levelname)s %(message)s',
             '%(levelname)s %(message)s',
             '%(asctime)s %(pathname)s %(module)s %(levelname)s %(message)s'
             ]

logging.basicConfig(level=config.configs.logging.level,
                    format=formatter[config.configs.logging.formatter_style])

Logger = logging.getLogger('')

if config.configs.logging.filelog:
    path, file = os.path.split(config.configs.logging.filename)
    if not os.path.exists(path):
        os.makedirs(path)
    filelog = logging.FileHandler(config.configs.logging.filename, config.configs.logging.filemode)
    filelog.setFormatter(logging.Formatter(formatter[int(config.configs.logging.formatter_style)]))
    filelog.setLevel(config.configs.logging.level)

    Logger.addHandler(filelog)

if __name__ == '__main__':
    Logger.debug('This is a debug message')
    Logger.info('This is an info message')
    Logger.warning('This is a warning message')
    Logger.error('This is an errer message')
    Logger.critical('This is a critical message')
