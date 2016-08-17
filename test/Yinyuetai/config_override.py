#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    config_override.py
    -----------------------------------------------------------------

    configs in this file will override default configs.

"""

configs = {
    'logging':{
        'level':'INFO',
        'formatter_style':0,
        'filemode':'w'
    },
    'spider':{
        'contentLimit':10,
        'catalogueLimit':5,
        'loadurllistfromfile':False
    }, 
}