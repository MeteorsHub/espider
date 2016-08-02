#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.parser
    ------------------------------------------------------------

    This file is used to parse data from datafile that are scrab via spider

"""

__author__ = 'MeterKepler'

import os
import json
from lxml import etree

from espider.log import *
from espider.util import *


class BaseParser(object):
    parserName = ''

    def __init__(self, contentType, primaryKey = None, contentPath = config.configs.spider.contentdatapath, openMethod = 'rb', openEncoding = None):
        if parserName == '':
            Logger.warning('You should define parserName for your parser! Espider is shutting down...')
            exit(1)
        self.contentType = contentType
        self.contentPath = contentPath
        self.fileList = getFileList(contentPath)
        if len(self.fileList) == 0:
            Logger.warning('there is no %s file in %s, please have a check' %(self.contentType, self.contentPath))
            return
        self.fileListFilter()
        self.openMethod = openMethod
        self.openEncoding = openEncoding
        self.dataList = []
        self.primaryValue = []
        self.primaryKey = primaryKey

    def startParseContent(self):
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
        Logger.critical('parseContent() without override! espider is shuting down...')
        exit(1)

    def saveData(self):
        if config.configs.parse.file:
            try:
                dataList = []
                try:
                    if os.path.exists(config.configs.parse.contentpath + config.configs.parse.contentfile):
                        dataList = readLinesFile(config.configs.parse.contentpath + config.configs.parse.contentfile)
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
                writeLinesFile(config.configs.parse.contentpath + config.configs.parse.contentfile, dataList, method=config.configs.parse.savemethod)
            except Exception as e:
                Logger.error('an error occured while saving data to file...', e)
        if config.configs.parse.mysql:
            from espider.mysql import Mysql
            keyList = []
            for k in self.dataList[0]:
                keyList.append(k)
            mySql = Mysql(config.configs.mysql.table, keyList, primaryKey=self.primaryKey)
            mySql.insertWithUpdate(self.dataList)



    def addDataItem(self, item, primaryKey):
        if primaryKey != None and primaryKey in item:
            if item[primaryKey] not in self.primaryValue:
                if self.primaryKey == None:
                    self.primaryKey = primaryKey
                elif self.primaryKey != primaryKey:
                    Logger.critical('different primary key found in returned data. espider is shutting down...')
                    exit(1)
                self.primaryValue.append(item[primaryKey])
                self.dataList.append(item)
            return
        self.dataList.append(item)

    def fileListFilter(self):
        for i in range(len(self.fileList)):
            if os.path.splitext(self.fileList[i])[1] !='.' + self.contentType :
                self.fileList.pop(i)
        return

class HtmlParser(BaseParser):
    def __init__(self, contentType = 'html', primaryKey = None, contentPath = config.configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(HtmlParser,self).__init__(contentType = contentType, primaryKey = primaryKey, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)

    def fileListFilter(self):
        for i in range(len(self.fileList)):
            if os.path.splitext(self.fileList[i])[1] not in ['.html', '.htm'] :
                self.fileList.pop(i)
        return

class XmlParser(BaseParser):
    def __init__(self, contentType = 'xml', contentPath = config.configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(XmlParser,self).__init__(contentType = contentType, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)

class JsonParser(BaseParser):
    def __init__(self, contentType = 'json', contentPath = config.configs.spider.contentdatapath, openMethod = 'r', openEncoding = 'utf8'):
        super(XmlParser,self).__init__(contentType = contentType, contentPath = contentPath, openMethod = openMethod, openEncoding = openEncoding)
