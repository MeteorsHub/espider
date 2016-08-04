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
    'mysql':{
        'table':'testlianjiajson'
    },
    'spider':{
        'contentLimit':5,
        'catalogueLimit':5
    },
    'http':{
        'proxy':True
    }
}