#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.spider
    ------------------------------------------------------------

    This file is used to scrab objective url and save as file

"""

__author__ = 'MeterKepler'

import os
import shutil
import random
import time
from urllib.parse import urlparse, quote, urljoin, urlunparse
from urllib import request
from lxml import etree
import json

from espider.httphandler import HttpHandler
from espider.log import *
from espider.util import *


class BaseSpider(object):
    __slots__ = ('host', 'httpHandler', 'catalogueUrl', 'contentUrl', 'catalogueCount', 'contentCount')
    espiderName = ''
    startUrl = ''

    def __init__(self):
        Logger.info('espider %s initiating...' %self.espiderName)
        if self.startUrl == '' or self.startUrl == '':
            Logger.critical('Your espider should have an espiderName and a startUrl! Espider is shutting down...')
            exit(1)
        self.startUrl = urlunparse(urlparse(self.startUrl, 'http'))
        if urlparse(self.startUrl).hostname == None:
            Logger.critical('Illegal url! Please make sure url like "http://www.baidu.com". Espider will be closed...')
            exit(1)
        self.host = urlparse(self.startUrl).scheme + '://' +urlparse(self.startUrl).hostname
        self.httpHandler = HttpHandler(self.host)
        if not os.path.exists(config.configs.spider.pipelinepath):
            os.makedirs(config.configs.spider.pipelinepath)
        self.catalogueUrl = set()
        self.catalogueCount = 0
        self.contentUrl = set()
        self.contentCount = 0


    def startEspider(self):
        Logger.info('start to get catalogue urls...')
        self.catalogueUrlRecursion(self.startUrl)
        writeLinesFile(config.configs.spider.cataloguefilename, self.catalogueUrl, method='w+')
        writeLinesFile(config.configs.spider.contentfilename, self.contentUrl, method='w+')
        count = 0
        for item in self.contentUrl:
            count = count + 1
            self.contentHandler(item, count)
        Logger.info('espider complete the task!')


    def catalogueUrlRecursion(self, url):
        if config.configs.spider.catalogueLimit != 'inf':
            if self.catalogueCount >= config.configs.spider.catalogueLimit:
                return
        url = urljoin(self.host, url)
        urllistContent = []
        urllistCatalogue = []
        for i in range(config.configs.spider.retry):
            response = self.httpHandler.getResponseByUrl(url)
            if response == None:
                Logger.warning('cannot get url %s. please check httphandler...' %url)
                return
            try:
                urllistCatalogue, urllistContent = self.getUrlList(response)
                break
            except ValueError:
                Logger.critical('please verify your getUrlList() return 2 lists. espider is shutting down...')
                exit(1)
            except Exception as e:
                Logger.error('an error occured in getUrlList(). if this take place often, please check your code')
                self.httpHandler.nextHandler()
        if(len(urllistContent) != 0):
            for item in urllistContent:
                self.contentCount = self.contentCount + 1
                if config.configs.spider.contentLimit != 'inf':
                    if self.contentCount >= config.configs.spider.contentLimit:
                        break
                if not item in self.contentUrl:
                    Logger.debug('discover content url %s' %item)
                    self.contentUrl.add(item)
        if len(urllistCatalogue) == 0:
            return
        else:
            for item in urllistCatalogue:
                if not item in self.catalogueUrl:
                    if config.configs.spider.catalogueLimit != 'inf':
                        if self.catalogueCount >= config.configs.spider.catalogueLimit:
                            return
                    Logger.info('get catalogue url %s' %item)
                    self.catalogueUrl.add(item)
                    self.catalogueCount = self.catalogueCount + 1
                    time.sleep(random.random()*config.configs.http.sleeptime)
                    self.catalogueUrlRecursion(item)
            return


    def getUrlList(self, response):
        Logger.critical('getUrlList() without override! espider is shuting down...')
        exit(1)

    def contentHandler(self, url, count):
        url = urljoin(self.host, url)
        Logger.info('(%s%%)get content data from %s' %(round(100*count/len(self.contentUrl), 2), url))
        data = None
        type = ''
        name = None
        for i in range(config.configs.spider.retry):
            response = self.httpHandler.getResponseByUrl(url)
            if response == None:
                Logger.warning('cannot get url %s. please check httphandler...' %url)
                return
            try:
                name = self.contentFileName(response)
                data, type = self.contentResponseHandle(response)
            except Exception as e:
                Logger.error('an error occured in getUrlList(). if this take place very often, please check your code')
                self.httpHandler.nextHandler()
        if name == None:
            name = '%s.' %count + type
        if data == None:
            return
        if not os.path.exists(config.configs.spider.contentdatapath):
            os.makedirs(config.configs.spider.contentdatapath)
        try:
            if type == 'html' or type == 'xml' or type == 'json' or type == 'js' or type == 'css':
                with open(config.configs.spider.contentdatapath + name, 'w+', encoding='utf8') as f:
                    f.write(data)
                return
            if type == 'jpg' or type == 'tif' or type == 'ico' or type == 'png' or type == 'bmp' or type == 'mp3' or type == 'avi' or type == 'mp4':
                with open(config.configs.spider.contentdatapath + name, 'wb+') as f:
                    f.write(data)
                return
            with open(config.configs.spider.contentdatapath + name, 'wb+') as f:
                f.write(data)
        except OSError:
            Logger.error('anerrer occured when open %s' %config.configs.spider.contentdatapath + name)
        return

    def contentFileName(self, response):
        return None

    def contentResponseHandle(self, response):
        type = response.getheader('Content-Type')
        if type == 'text/html':
            return (response.read().decode('utf8'), 'html')
        if type == 'text/xml':
            return (response.read().decode('utf8'), 'xml')
        if type == 'application/json':
            return (response.read().decode('utf8'), 'json')
        if type == 'application/javascript' or  type == 'application/ecmascript':
            return (response.read().decode('utf8'), 'js')
        if type == 'image/jpeg':
            return (response.read(), 'jpg')
        if type == 'image/tiff':
            return (response.read(), 'tif')
        if type == 'image/x-icon':
            return (response.read(), 'ico')
        if type == 'image/png':
            return (response.read(), 'png')
        if type == 'text/css':
            return (response.read().decode('utf8'), 'css')
        if type == 'application/x-bmp':
            return (response.read(), 'bmp')
        if type == 'audio/mp3':
            return (response.read(), 'mp3')
        if type == 'video/avi':
            return (response.read(), 'avi')
        if type == 'video/mpeg4':
            return (response.read(), 'mp4')
        return (response.read(), '')

class UrlQuerySpider(BaseSpider):
    __slots__ = ('host', 'baseUrl', 'queryList', 'parameterList','extraParameter' 'level')

    def __init__(self, baseUrl, queryList, parameterList, extraParameter = {}):
        Logger.info('Espider %s initiating...' %self.espiderName)
        if urlparse(baseUrl).hostname == None:
            Logger.critical('Illegal url! Please make sure url like "http://www.baidu.com". Espider will be closed...')
            exit(1)
        self.host = urlparse(baseUrl).scheme + '://' +urlparse(baseUrl).hostname
        self.baseUrl = baseUrl
        self.queryList = queryList
        self.parameterList = parameterList
        self.extraParameter = extraParameter
        self.level = 1
        self.checkUrlQuery()
        self.httpHandler = HttpHandler(self.host)

    def startEspider(self):
        Logger.info('starting espider...')
        paramList = readLinesFile(config.configs.spider.contentdatapath + 'param.txt')
        if paramList == None:
            return
        for i in range(len(paramList)):
            paramList[i] = json.loads(paramList[i])
            for k,v in paramList[i].items():
                if k in self.parameterList[0]:
                    param = {}
                    param[k] = v
                    path = config.configs.spider.contentdatapath + k + '=' + v + '/'
                    self.catalogueUrlRecursion(param, path, 1)
                else:
                    Logger.error('param.txt gives an incorrect key compared to self.paramterList...')


    def catalogueUrlRecursion(self, param, path, level):
        if not os.path.exists(path):
            os.makedirs(path)
        Logger.info('(level %s)start to scrab param:%s' %(level, param))
        if isinstance(self.queryList[level - 1], list):
            for query in self.queryList[level - 1]:
                url = self.buildUrl(query, param)
                response = self.httpHandler.getResponseByUrl(url)
                data, type = self.contentResponseHandle(response)
                with open(path + 'data_query=' + query + '.' + type, 'w+', encoding='utf8') as f:
                    f.write(data)
                if level == self.level:
                    continue
                nextParamList = self.contentHandler(data)
                if nextParamList == None or nextParamList == []:
                    return
                if not isinstance(nextParamList, list):
                    Logger.critical('contentHandler() should return a list. Espider is shutting down...')
                    exit(1)
                if not isinstance(nextParamList[0], dict):
                    Logger.critical('contentHandler() should return list made by dict of each element. Espider is shutting down...')
                    exit(1)
                writeLinesFile(path + 'param_query='+ query + '.txt', nextParamList)
                for nextParam in nextParamList:
                    for k,v in nextParam:
                        if k in self.parameterList[level]:
                            nextParamDict = param
                            nextParamDict[k] = v
                            nextPath = path + k + '=' + v + '/'
                            time.sleep(random.random()*config.configs.http.sleeptime)
                            self.catalogueUrlRecursion(nextParamDict, nextPath, level + 1)
                        else:
                            Logger.error('param.txt gives an incorrect key %s compared to self.paramterList(level %s)...' %(k, level))
        else:
            query = self.queryList[level - 1]
            url = self.buildUrl(query, param)
            response = self.httpHandler.getResponseByUrl(url)
            data, type = self.contentResponseHandle(response)
            with open(path + 'data_query=' + query + '.' + type, 'w+', encoding='utf8') as f:
                f.write(data)
            if level == self.level:
                return
            try:
                nextParamList = self.contentHandler(data)
            except Exception:
                Logger.error('an error occured in contentHandler(). If this take place often, please shut espider down...')
                nextParamList = None
            if nextParamList == None or nextParamList == []:
                return
            if not isinstance(nextParamList, list):
                Logger.critical('contentHandler() should return a list. Espider is shutting down...')
                exit(1)
            if not isinstance(nextParamList[0], dict):
                Logger.critical('contentHandler() should return list made by dict of each element. Espider is shutting down...')
                exit(1)
            writeLinesFile(path + 'param_query='+ query + '.txt', nextParamList)
            for nextParam in nextParamList:
                for k,v in nextParam.items():
                    if k in self.parameterList[level]:
                        nextParamDict = dict(param)
                        nextParamDict[k] = v
                        nextPath = path + k + '=' + v + '/'
                        time.sleep(random.random()*config.configs.http.sleeptime)
                        self.catalogueUrlRecursion(nextParamDict, nextPath, level + 1)
                    else:
                        Logger.error('param.txt gives an incorrect key %s compared to self.paramterList(level %s)...' %(k, level))


    def contentHandler(self, data):
        Logger.critical('contentHandler() without override! espider is shuting down...')
        exit(1)


    def buildUrl(self, query, param):
        queryList = []
        for k,v in self.extraParameter.items():
            queryList.append(k + '=' + v)
        for k,v in param.items():
            queryList.append(k + '=' + v)
        url = self.baseUrl + query + '?' + '&'.join(queryList)
        return url



    def checkUrlQuery(self):
        if not isinstance(self.queryList, list):
            Logger.critical('Illegal queryList, you need define it as a list. Espider is shutting down...')
            exit(1)
        if not isinstance(self.parameterList, list):
            Logger.critical('Illegal parameterList, you need define it as a list. Espider is shutting down...')
            exit(1)
        if len(self.queryList) != len(self.parameterList):
            Logger.critical('Different length of queryList and parameterList, please make sure they match each other. Espider is shutting down...')
            exit(1)
        self.level = len(self.queryList)
        if not isinstance(self.extraParameter, dict):
            Logger.critical('Illegal extraParameter, you need define it as a dict. Espider is shutting down...')
            exit(1)

class GsExtractor(object):
    def _init_(self):
        self.xslt = ""

    # 从文件读取xslt
    def setXsltFromFile(self , xsltFilePath):
        file = open(xsltFilePath , 'r' , encoding='utf8')
        try:
            self.xslt = file.read()
        finally:
            file.close()

    # 从字符串获得xslt
    def setXsltFromMem(self , xsltStr):
        self.xslt = xsltStr

    # 通过GooSeeker API接口获得xslt
    def setXsltFromAPI(self , APIKey , theme, middle=None, bname=None):
        apiurl = "http://www.gooseeker.com/api/getextractor?key="+ APIKey +"&theme="+quote(theme)
        if (middle):
            apiurl = apiurl + "&middle="+quote(middle)
        if (bname):
            apiurl = apiurl + "&bname="+quote(bname)
        apiconn = request.urlopen(apiurl)
        self.xslt = apiconn.read()

    # 返回当前xslt
    def getXslt(self):
        return self.xslt

    # 提取方法，入参是一个HTML DOM对象，返回是提取结果
    def extract(self , html):
        xslt_root = etree.XML(self.xslt)
        transform = etree.XSLT(xslt_root)
        result_tree = transform(html)
        return result_tree