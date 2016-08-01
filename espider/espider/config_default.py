#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.conf.config_default.py
    ---------------------------------------------------------------------------------------

    set up default config, if you wan't to change this, please change in config_override.py

"""

configs = {
    'logging':{
        'level':'INFO',
        'filelog':True,
        'formatter_style':0,
        'filename':'resources/espider.log',
        'filemode':'a'
    },
    'mysql':{
        'host':'localhost',
        'user':'root',
        'password':'123456',
        'db':'espider',
        'table':'default'
    },
    'proxy':{
        'rescrab':False,
        'retest':False,
        'srcname':'resources/proxy.pro',
        'mode':1,
        'timeout':3,
        'proxysrc':2,
        'srcpage':1
    },
    'urlrequest':{
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    },
    'http':{
        'sleeptime':1,
        'timeout':5,
        'retry':3,
        'proxy':False,
        'selephan':True
    },
    'selephan':{
        'timeout':5,
        'loadimages':False
    },
    'spider':{
        'retry':3,
        'catalogueLimit':'inf',
        'contentLimit':'inf',
        'pipelinepath':'pipeline/',
        'cataloguefilename':'pipeline/catalogueUrl.txt',
        'contentfilename':'pipeline/contentUrl.txt',
        'contentdatapath':'pipeline/data/'
    },
    'parse':{
        'file':True,
        'contentpath':'pipeline/parsedData/',
        'contentfile':'dataDict.txt',
        'savemethod':'w+',
        'mysql':True
    }
}