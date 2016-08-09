#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.tools.proxyupdate
    ------------------------------------------------------------

    This file is used to update proxy lib regularly. 
    If you want to update your proxy list, just use function proxyUpdate(url=None)

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeteorKepler'

from espider.proxy import *
from espider.config import configs
from espider.log import Logger

__all__ = [
    'proxyUpdate',
    ]

def proxyUpdate(url = None):
    """
        A tool for proxy list updating. 
        Input url is the checking url for testing proxy. Default url is 'http://www.baidu.com'
    """

    if url == None:
        url = 'http://www.baidu.com'
    temp1 = configs.proxy.rescrab
    temp2 = configs.proxy.retest
    # override configs
    configs.proxy.rescrab = True
    configs.proxy.retest = True
    # update proxy
    updateProxy = Proxy(url)
    # resume original configs
    configs.proxy.rescrab = temp1
    configs.proxy.retest = temp2
