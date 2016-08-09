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

from collections import Iterable
import os

from espider.config import configs
from espider.log import Logger


__all__ = ['readLinesFile', 
           'writeLinesFile', 
           'getFileList', 
           'json_get',
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