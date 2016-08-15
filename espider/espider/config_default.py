#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.conf.config_default.py
    ---------------------------------------------------------------------------------------

    Set up default config, if you wan't to change some configs, please do so in 
    config_override.py in your project path.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeteorKepler'

__all__ = [
    'configs',
    ]

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
        'port':3316,
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
        'User-Agent':['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
                      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
                      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
                      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
        ]
    },
    'http':{
        'sleeptime':0.4,
        'timeout':5,
        'retry':3,
        'proxy':False,
        'selephan':False
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
        'contentupdatefilename':'pipeline/contentUpdateList.txt',
        'contentbackuppath':'pipeline/backup/',
        'contentdatapath':'pipeline/data/',
        'mode':'override'
    },
    'parse':{
        'file':True,
        'contentpath':'pipeline/parsedData/',
        'contentfile':'dataDict.txt',
        'savemethod':'w+',
        'mysql':False
    }
}