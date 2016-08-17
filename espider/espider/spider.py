#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.spider
    ------------------------------------------------------------

    This file is used to scrab objective url and save as file
    Also provides class that manipulate UrlQuery spider.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import os
import shutil
import random
import time
from datetime import datetime
from urllib.parse import urlparse, quote, urljoin, urlunparse
from urllib import request
import json
from collections import OrderedDict


from espider.httphandler import HttpHandler
from espider.util import *
from espider.config import configs
from espider.log import Logger
from espider.parser import *

__all__ = [
    'BaseSpider',
    'UrlQuerySpider',
    'GsExtractor',
    ]


class BaseSpider(object):
    """
        Basic spider that needs defination of espiderName and startUrl.
        Also need to override getUrlList().
        You can also override buildExtraHeaders() but this is not necessary which aims to add 
        different headers according to different url.
    """
    __slots__ = ('host', 'httpHandler', 'catalogueUrl', 'contentDictList', 'catalogueCount', 'contentCount', 'uncatchableUrlList')
    espiderName = ''
    startUrl = ''
    parser = None

    def __init__(self):
        Logger.info('espider %s initiating...' % self.espiderName)
        if self.startUrl == '' or self.espiderName == '':
            Logger.critical('Your espider should have an espiderName and a startUrl! Espider is shutting down...')
            exit(1)
        self.startUrl = urlunparse(urlparse(self.startUrl, 'http'))
        if urlparse(self.startUrl).hostname == None:
            Logger.critical('Illegal url! Please make sure url like "http://www.baidu.com". Espider will be closed...')
            exit(1)
        self.host = urlparse(self.startUrl).scheme + '://' + urlparse(self.startUrl).hostname
        self.httpHandler = HttpHandler(self.host)
        if not os.path.exists(configs.spider.pipelinepath):
            os.makedirs(configs.spider.pipelinepath)
        self.catalogueUrl = set()
        self.catalogueCount = 0
        self.contentCount = 0
        self.contentDictList = []
        self.uncatchableUrlList = []



    def startEspider(self):
        if configs.spider.mode != 'override' and configs.spider.mode != 'update':
            Logger.error('Please verify spider.mode is override or update in configs. Spider will run in default mode(override)')
        if configs.spider.mode == 'update' and self.parser == None:
            Logger.error('Spider cannot run in update mode without a correct function setParser() defined. ')
        Logger.info('Espider running in %s mode' %('override' if self.parser == None else 'update'))
        if self.parser != None:
            # update mode
            self.backupUpdate()
            self.contentDictList = self.loadContentDictList()

        Logger.info('start to get catalogue urls...')

        if configs.spider.loadurllistfromfile:
            self.loadCatalogueList()
            self.contentDictList = self.loadContentDictList()
        else:
            self.catalogueUrlRecursion(self.startUrl)
            writeLinesFile(configs.spider.cataloguefilename, self.catalogueUrl, method='w+')
        count = 0

        for item in self.contentDictList:
            count = count + 1
            MD5, filepath = self.contentHandler(item['contentUrl'], count)
            item['filepath'] = filepath
            if 'MD5' in item:
                if self.parser == None:
                    item['update'] = 'disabled'
                elif item['MD5'] == MD5:
                    item['update'] = 'false'
                else:
                    item['update'] = 'true'
                item['MD5'] = MD5
            else:
                if self.parser == None:
                    item['update'] = 'disabled'
                else:
                    item['update'] = 'true'
                item['MD5'] = MD5
        self.saveContentUrlDictList()
        self.saveContentUrlUpdate()
        Logger.info('espider complete the task!')

    def setParser(self, parser):
        if configs.spider.mode == 'override':
            Logger.warning('Spider mode is override in configs. setParse() will be ignored. If you want to use update mode, change it in config_override')
            return
        if not isinstance(parser, BaseParser):
            Logger.error('setParser() should have a BaseParser-like object input. Spider will scribe in override instead of update mode')
            return
        self.parser = parser

    def loadContentDictList(self):
        if not os.path.exists(configs.spider.contentfilename):
            return []
        dataList = readLinesFile(configs.spider.contentfilename)
        dataDictList = []
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

    def backupUpdate(self):
        if not os.path.exists(configs.spider.contentfilename):
            return
        if not os.path.exists(configs.spider.contentbackuppath):
            os.makedirs(configs.spider.contentbackuppath)
        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_')
        dstfilename = os.path.join(configs.spider.contentbackuppath, now + os.path.split(configs.spider.contentupdatefilename)[1])
        try:
            shutil.copy2(configs.spider.contentupdatefilename, dstfilename)
        except IOError:
            Logger.error('Cannot copy file to update path...')

    def saveContentUrlDictList(self):
        instruction = '# contentUrl\tMD5\tupdate\tfilepath'
        dataList = []
        dataList.append(instruction)
        for item in self.contentDictList:
            temp = '%s\t%s\t%s\t%s' %(item['contentUrl'], item['MD5'], item['update'], item['filepath'])
            dataList.append(temp)
        writeLinesFile(configs.spider.contentfilename, dataList, method='w+')

    def saveContentUrlUpdate(self):
        if self.parser == None:
            return
        instruction = '# contentUrl\tMD5\tupdate\tfilepath'
        dataList = []
        dataList.append(instruction)
        for item in self.contentDictList:
            if item['update'] == 'true':
                temp = '%s\t%s\t%s\t%s' %(item['contentUrl'], item['MD5'], item['update'], item['filepath'])
                dataList.append(temp)
        writeLinesFile(configs.spider.contentupdatefilename, dataList, method='w+')

    def catalogueUrlRecursion(self, url):
        if configs.spider.catalogueLimit != 'inf':
            if self.catalogueCount >= configs.spider.catalogueLimit:
                return
        url = urljoin(self.host, url)
        urllistContent = []
        urllistCatalogue = []
        for i in range(configs.spider.retry):
            response = self.httpHandler.getResponseByUrl(url)
            if response == None:
                Logger.warning('cannot get url %s. please check httphandler...' % url)
                return
            response = EsResponse(response)
            try:
                urllistCatalogue, urllistContent = self.getUrlList(response)               
                break
            except ValueError:
                Logger.critical('please verify your getUrlList() return 2 lists. espider is shutting down...')
                exit(1)
            except Exception as e:
                Logger.error('an error occured in getUrlList(). if this take place often, please check your code')
                self.httpHandler.nextHandler()
                if i == configs.spider.retry - 1:
                    self.uncatchableUrlList.append(url)
                    self.saveUncatchableUrl()
        if(len(urllistContent) != 0):
            for item in urllistContent:
                self.contentCount = self.contentCount + 1
                if configs.spider.contentLimit != 'inf':
                    if self.contentCount > configs.spider.contentLimit:
                        break
                if not keyValueInDictList('contentUrl', item, self.contentDictList):
                    Logger.debug('discover content url %s' % item)
                    dictTemp = {}
                    dictTemp['contentUrl'] = item
                    self.contentDictList.append(dictTemp)
        if len(urllistCatalogue) == 0:
            return
        else:
            for item in urllistCatalogue:
                if not item in self.catalogueUrl:
                    if configs.spider.catalogueLimit != 'inf':
                        if self.catalogueCount >= configs.spider.catalogueLimit:
                            return
                    Logger.info('get catalogue url %s' % item)
                    self.catalogueUrl.add(item)
                    self.catalogueCount = self.catalogueCount + 1
                    time.sleep(random.random() * configs.http.sleeptime)
                    self.catalogueUrlRecursion(item)
            return

    def loadCatalogueList(self):
        self.catalogueUrl = readLinesFile(configs.spider.cataloguefilename)
        return

    def saveUncatchableUrl(self):
        if len(self.uncatchableUrlList) == 0:
            return
        writeLinesFile(configs.spider.uncatchableurlfilename, self.uncatchableUrlList, method='w+')


    def getUrlList(self, response):
        Logger.critical('getUrlList() without override! espider is shuting down...')
        exit(1)

    def contentHandler(self, url, count):
        url = urljoin(self.host, url)
        Logger.info('(%s%%)get content data from %s' % (round(100 * count / len(self.contentDictList), 2), url))
        data = None
        type = ''
        name = None
        for i in range(configs.spider.retry):
            response = self.httpHandler.getResponseByUrl(url)
            if response == None:
                Logger.warning('cannot get url %s. please check httphandler...' % url)
                return ('disabled', 'disabled')
            response = EsResponse(response)
            try:
                data, type = self.contentResponseHandle(response)
                if data == None:
                    Logger.debug('data == None')
                    raise Exception
                
                name = self.contentFileName(response)
            except Exception:
                Logger.error('an error occured in getUrlList(). if this take place very often, please check your code')
                self.httpHandler.nextHandler()
                if i == configs.spider.retry - 1:
                    self.uncatchableUrlList.append(url)
                    self.saveUncatchableUrl()
                continue
            break
        if data == None:
            return ('disabled', 'disabled')
        if name == None:
            name = '%s.' % count + type
        if not os.path.exists(configs.spider.contentdatapath):
            os.makedirs(configs.spider.contentdatapath)
        if self.parser == None:
            MD5 = buildMD5String(data)
        else:
            try:
                parsedData = '%s' %self.parser.parseContent(data)
                MD5 = buildMD5String(parsedData)
            except Exception:
                Logger.error('An error occured in parseContent()! Please check your code. Espider will use the whole file as update md5')
                MD5 = buildMD5String(data)
        filepath = configs.spider.contentdatapath + name
        try:
            if type == 'html' or type == 'xml' or type == 'json' or type == 'js' or type == 'css':
                with open(filepath, 'w+', encoding='utf8') as f:
                    f.write(data)
                return (MD5, filepath)
            if type == 'jpg' or type == 'tif' or type == 'ico' or type == 'png' or type == 'bmp' or type == 'mp3' or type == 'avi' or type == 'mp4':
                with open(filepath, 'wb+') as f:
                    f.write(data)
                return (MD5, filepath)
            with open(filepath, 'wb+') as f:
                f.write(data)
        except OSError:
            Logger.error('anerrer occured when open %s' % configs.spider.contentdatapath + name)
        return (MD5, filepath)

    def contentFileName(self, response):
        return None

    def buildExtraHeaders(self, url):
        return (url, {})

    def contentResponseHandle(self, response):
        type = response.getheader('Content-Type')
        if not self.contentAvailable(response):
            return (None, None)
        if 'text/html' in type:
            return (response.read().decode('utf8'), 'html')
        if 'text/xml' in type:
            return (response.read().decode('utf8'), 'xml')
        if 'application/json' in type:
            return (response.read().decode('utf8'), 'json')
        if 'application/javascript' in type or 'application/ecmascript' in type:
            return (response.read().decode('utf8'), 'js')
        if 'image/jpeg' in type:
            return (response.read(), 'jpg')
        if 'image/tiff' in type:
            return (response.read(), 'tif')
        if 'image/x-icon' in type:
            return (response.read(), 'ico')
        if 'image/png' in type:
            return (response.read(), 'png')
        if 'text/css' in type:
            return (response.read().decode('utf8'), 'css')
        if 'application/x-bmp' in type:
            return (response.read(), 'bmp')
        if 'audio/mp3' in type:
            return (response.read(), 'mp3')
        if 'video/avi' in type:
            return (response.read(), 'avi')
        if 'video/mpeg4' in type:
            return (response.read(), 'mp4')
        return (response.read(), '')

    def contentAvailable(self, response):
        """
        You can override this method to check whether the content page is available
        """
        return True

class UrlQuerySpider(BaseSpider):
    """
        Different objectives from BaseSpider.
        Build url query in tree structure.
    """
    __slots__ = ('host', 'level')
    queryList = []
    parameterList = []
    extraParameter = OrderedDict()

    def __init__(self):
        Logger.info('Espider %s initiating...' % self.espiderName)
        if self.startUrl == '':
            Logger.critical('Your espider should have a startUrl! Espider is shutting down...')
            exit(1)
        self.startUrl = urlunparse(urlparse(self.startUrl, 'http'))
        if urlparse(self.startUrl).hostname == None:
            Logger.critical('Illegal url! Please make sure url like "http://www.baidu.com". Espider will be closed...')
            exit(1)
        self.host = urlparse(self.startUrl).scheme + '://' + urlparse(self.startUrl).hostname
        self.checkUrlQuery()
        self.httpHandler = HttpHandler(self.host)

    def startEspider(self):
        Logger.info('starting espider...')
        paramList = readLinesFile(configs.spider.contentdatapath + 'param.txt')
        if paramList == None:
            Logger.critical('You should create starting parameters in %s' % (configs.spider.contentdatapath + 'param.txt'))
            exit(1)
        for i in range(len(paramList)):
            paramList[i] = json.loads(paramList[i])
            for k,v in paramList[i].items():
                if k in self.parameterList[0]:
                    param = {}
                    param[k] = v
                    path = configs.spider.contentdatapath + k + '=' + v + '/'
                    self.catalogueUrlRecursion(param, path, 1)
                else:
                    Logger.error('param.txt gives an incorrect key compared to self.paramterList...')


    def catalogueUrlRecursion(self, param, path, level):
        if not os.path.exists(path):
            os.makedirs(path)
        Logger.info('(level %s)start to scrab param:%s' % (level, param))
        if not isinstance(self.queryList[level - 1], list):
            self.queryList[level - 1] = [self.queryList[level - 1]]
        for query in self.queryList[level - 1]:
            url = self.buildUrl(query, param)
            url, headers = self.buildExtraHeaders(url)
            response = self.httpHandler.getResponseByUrl(url, headers=headers)
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
            writeLinesFile(path + 'param_query=' + query + '.txt', nextParamList)
            for nextParam in nextParamList:
                for k,v in nextParam.items():
                    if k in self.parameterList[level]:
                        nextParamDict = dict(param)
                        nextParamDict[k] = v
                        nextPath = path + k + '=' + v + '/'
                        time.sleep(random.random() * configs.http.sleeptime)
                        self.catalogueUrlRecursion(nextParamDict, nextPath, level + 1)
                    else:
                        pass


    def contentHandler(self, data):
        Logger.critical('contentHandler() without override! espider is shuting down...')
        exit(1)


    def buildUrl(self, query, param):
        queryList = []
        for k,v in self.extraParameter.items():
            queryList.append(k + '=' + v)
        for k,v in param.items():
            queryList.append(k + '=' + v)
        url = self.startUrl + query + '?' + '&'.join(queryList)
        return url



    def checkUrlQuery(self):
        if not isinstance(self.queryList, list) or len(self.queryList) == 0:
            Logger.critical('Please define queryList as a non-empty list! Espider is shutting down...')
            exit(1)
        if not isinstance(self.parameterList, list) or len(self.parameterList) == 0:
            Logger.critical('Please define parameterList as a non-empth list! Espider is shutting down...')
            exit(1)
        if not isinstance(self.extraParameter, OrderedDict):
            Logger.critical('extraParameter should be OrderedDict! Espider is shutting down')
            exit(1)
        if len(self.queryList) != len(self.parameterList):
            Logger.critical('Different length of queryList and parameterList, please make sure they match each other. Espider is shutting down...')
            exit(1)
        self.level = len(self.queryList)

class GsExtractor(object):
    """
        Helping class if you want to extract data with the method of xslt.
        This is associated with GooSeeker tool.
    """
    def _init_(self):
        from lxml import etree
        self.xslt = ""

    def setXsltFromFile(self , xsltFilePath):
        file = open(xsltFilePath , 'r' , encoding='utf8')
        try:
            self.xslt = file.read()
        finally:
            file.close()

    def setXsltFromMem(self , xsltStr):
        self.xslt = xsltStr

    def setXsltFromAPI(self , APIKey , theme, middle=None, bname=None):
        apiurl = "http://www.gooseeker.com/api/getextractor?key=" + APIKey + "&theme=" + quote(theme)
        if (middle):
            apiurl = apiurl + "&middle=" + quote(middle)
        if (bname):
            apiurl = apiurl + "&bname=" + quote(bname)
        apiconn = request.urlopen(apiurl)
        self.xslt = apiconn.read()

    def getXslt(self):
        return self.xslt

    def extract(self , html):
        xslt_root = etree.XML(self.xslt)
        transform = etree.XSLT(xslt_root)
        result_tree = transform(html)
        return result_tree

    