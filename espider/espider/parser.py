#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.parser
    ------------------------------------------------------------

    This module is used to parse data from datafile that are scrab via spider.


    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import json
import os
from collections import OrderedDict

from espider.util import *
from espider.config import configs
from espider.log import Logger

__all__ = [
    'BaseParser',
    'HtmlParser',
    'XmlParser',
    'JsonParser',
    ]


class BaseParser(object):
    """
        Basic parser that provide saving data to file and mysql service.
        The user must override function parseContent().
    """
    parserName = ''

    def __init__(self, contentType, primaryKey = None, contentPath = configs.spider.contentdatapath, openMethod = 'rb', openEncoding = None):
        if self.parserName == '':
            Logger.warning('You should define parserName for your parser! Espider is shutting down...')
            exit(1)
        self.contentType = contentType
        self.contentPath = contentPath
        self.openMethod = openMethod
        self.openEncoding = openEncoding
        self.dataList = []
        self.primaryValue = []
        self.primaryKey = primaryKey
        self.contentPath = contentPath

    def startParseContent(self):
        self.fileList = getFileList(self.contentPath)
        if len(self.fileList) == 0:
            Logger.warning('There is no %s file in %s, please have a check' %(self.contentType, self.contentPath))
            return
        self.fileListFilter()
        Logger.info('starting parsing content...')
        if len(self.fileList) == 0:
            return
        dataDict = []
        for i in range(len(self.fileList)):
            try:
                try:
                    with open(self.fileList[i], self.openMethod, encoding=self.openEncoding) as f:
                        data = f.read()
                    dataDict = self.parseContent(data)
                except OSError:
                    Logger.error('an error occured when open %s' %self.fileList[i])
                    continue
            except Exception:
                Logger.error('an error occured when parsing content. If this takes place very often, please check your parseContent()...')
                continue
            if not isinstance(dataDict, list):
                Logger.error('please make sure parseContent() returns an list-like object')
                continue
            if len(dataDict) == 0:
                continue
            for item in dataDict:
                if not isinstance(item, dict):
                    Logger.error('please make sure parseContent() returns dict-like objects in each element of a list. if this occur often, please teminate progress...')
                self.addDataItem(item, self.primaryKey)
        self.saveData()
        Logger.info('parsing content done')


    def parseContent(self, data):
        """
            data is a bytes type variable, you should return a list with each element of dict type
        """
        Logger.critical('parseContent() without override! espider is shuting down...')
        exit(1)

    def saveData(self):
        if configs.parse.file:
            try:
                dataList = []
                try:
                    if os.path.exists(configs.parse.contentpath + configs.parse.contentfile):
                        dataList = readLinesFile(configs.parse.contentpath + configs.parse.contentfile)
                        for i in range(len(dataList)):
                            try:
                                self.addDataItem(json.loads(dataList[i]), self.primaryKey)
                            except Exception:
                                pass
                except Exception:
                    pass
                dataList = []
                for item in self.dataList:
                    dataList.append(json.dumps(item, ensure_ascii = False))
                writeLinesFile(configs.parse.contentpath + configs.parse.contentfile, dataList, method=configs.parse.savemethod)
            except Exception as e:
                Logger.error('an error occured while saving data to file...', e)
        if configs.parse.mysql:
            from espider.mysql import Mysql
            keyList = []
            for k in self.dataList[0]:
                keyList.append(k)
            mySql = Mysql(configs.mysql.table, keyList, primaryKey=self.primaryKey)
            mySql.insertWithUpdate(self.dataList)



    def addDataItem(self, item, primaryKey):
        itemtemp = OrderedDict()
        for k,v in item.items():
            if isinstance(v, list):
                if len(v) == 0:
                    itemtemp[k] = ''
                else:
                    itemtemp[k] = v[0]
            else:
                itemtemp[k] = v
        if primaryKey != None and primaryKey in itemtemp:
            if itemtemp[primaryKey] not in self.primaryValue:
                if self.primaryKey == None:
                    self.primaryKey = primaryKey
                elif self.primaryKey != primaryKey:
                    Logger.critical('different primary key found in returned data. espider is shutting down...')
                    exit(1)
                self.primaryValue.append(itemtemp[primaryKey])
                self.dataList.append(itemtemp)
            return
        self.dataList.append(itemtemp)

    def fileListFilter(self):
        if configs.spider.mode == 'update':
            pass
        for i in range(len(self.fileList)):
            if os.path.splitext(self.fileList[i])[1] !='.' + self.contentType :
                self.fileList.pop(i)
        return

    def loadContentUpdateDictList(self):
        if not os.path.exists(configs.spider.contentupdatefilename):
            return []
        dataList = readLinesFile(configs.spider.contentfilename)
        fileList = []
        try:
            for item in dataList:
                if item.startswith('#'):
                    continue
                t = {}
                data = item.split('\t')
                t['contentUrl'] = data[0]
                t['MD5'] = data[1]
                t['update'] = data[2]
                t['filepath'] = data[3]
                dataDictList.append(t)
        except IndexError:
            Logger.error('Loading contentfile error!')
        return dataDictList

class HtmlParser(BaseParser):
    def __init__(self, contentType = 'html', primaryKey = None, contentPath = configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(HtmlParser,self).__init__(contentType = contentType, primaryKey = primaryKey, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)

    def fileListFilter(self):
        for i in range(len(self.fileList)):
            if os.path.splitext(self.fileList[i])[1] not in ['.html', '.htm'] :
                self.fileList.pop(i)
        return

class XmlParser(BaseParser):
    def __init__(self, contentType = 'xml', contentPath = configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(XmlParser,self).__init__(contentType = contentType, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)

class JsonParser(BaseParser):
    def __init__(self, contentType = 'json', contentPath = configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(XmlParser,self).__init__(contentType = contentType, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)
