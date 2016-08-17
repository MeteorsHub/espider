#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    espider.uril
    -------------------------------------------------------
    include utilities fucntion

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeteorKepler'

import os
import hashlib
from collections import Iterable
from http.client import HTTPResponse

from espider.config import configs
from espider.log import Logger


__all__ = ['readLinesFile', 
           'writeLinesFile', 
           'getFileList', 
           'json_get',
           'keyValueInDictList',
           'buildMD5String',
           'EsResponse',
           ]

def readLinesFile(filename, method = 'r'):
    """
        Read from a file and extract each line to the element of a list.
    """
    dataInLine = []
    try:
        with open(filename, method, encoding='utf8') as f:
            data = f.readlines()
            for i in range(len(data)):
                data[i] = data[i].strip()
            dataInLine = data
    except OSError:
        Logger.error('an errer occured when open %s' %filename)
        return None
    return dataInLine

def writeLinesFile(filename, dataInLine, method = 'w'):
    """
        Write a list to the file. One element to one line.
    """
    if not isinstance(dataInLine, Iterable):
        Logger.error('input illegal')
        return
    if not os.path.exists(os.path.split(filename)[0]):
        os.makedirs(os.path.split(filename)[0])
    dataInLine = [str(line) + '\n' for line in dataInLine]
    try:
        with open(filename, method, encoding = 'utf8') as f:
            f.writelines(dataInLine)
    except OSError:
        Logger.error('an errer occured when open %s' %filename)
    return

def getFileList(dir):
    """
        Find all files in dir and its sub-dirs.
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    fileList = []
    newdir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for item in os.listdir(dir):
            newdir = os.path.join(dir, item)
            filelist = getFileList(newdir)
            for it in filelist:
                fileList.append(it)
    return fileList

def json_get(js, key):
    """
        Find all element of key in json js, regardless of which level they are.
    """
    if not isinstance(key, str):
        return None
    ret = []
    for k,v in js.items():
        if isinstance(v, dict):
            temp = json_get(v, key)
            for item in temp:
                ret.append(item)
        elif isinstance(v, list):
            for item in v:
                temp = json_get(item, key)
                for it in temp:
                    ret.append(it)
        else:
            if k == key:
                ret.append(v)
    return ret

def keyValueInDictList(key, value, dictList):
    """
        Return a boolean whether a key-value data in dictList
        'dictList' is a list whose elements are dicts
    """
    if not isinstance(dictList, list):
        return False
    for item in dictList:
        if not isinstance(item, dict):
            continue
        if key in item:
            if value == item[key]:
                return True
    return False

def buildMD5String(data):
    md5 = hashlib.md5()
    if isinstance(data, str):
        md5.update(data.encode('utf8'))
    if isinstance(data, bytes):
        md5.update(data)
    return md5.hexdigest()

class EsResponse(object):
        """
            Built to make http.client.HTTPResponse can be read several times.
        """
        def __init__(self, response):
            self.data = b''
            self.headers = []
            self.code = ''
            if response == None:
                return
            if not isinstance(response, HTTPResponse):
                Logger.error('EsRequest error: wrong type of response')
                return
            self.data = response.read()
            self.headers = response.getheaders()
            self.code = response.getcode()
            self.url = response.geturl()

        def read(self):
            return self.data

        def getcode(self):
            return self.code

        def geturl(self):
            return self.url

        def getheaders(self):
            return self.headers

        def getheader(self, name, default=None):
            for item in self.headers:
                if name == item[0]:
                    return item[1]
            return default