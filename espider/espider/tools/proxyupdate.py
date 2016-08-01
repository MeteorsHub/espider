#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.tools.proxyupdate
    ------------------------------------------------------------

    This file is used to update proxy lib regularly

"""

__author__ = 'MeteorKepler'

from espider.proxy import *

def proxyUpdate(url = None):
    if url == None:
        url = 'http://www.baidu.com'
    temp1 = config.configs.proxy.rescrab
    temp2 = config.configs.proxy.retest
    config.configs.proxy.rescrab = True
    config.configs.proxy.retest = True
    updateProxy = Proxy(url)
    config.configs.proxy.rescrab = temp1
    config.configs.proxy.retest = temp2
