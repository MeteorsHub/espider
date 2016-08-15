#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.proxy
    ------------------------------------------------------------

    This file is about proxy handler via scrab.
    In espider, Proxy is used in HttpHandler.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeteorKepler'

import re
import os
import time
import urllib.error
import urllib.request
from random import randint

from espider.util import readLinesFile, writeLinesFile
from espider.config import configs
from espider.log import Logger

__all__ = [
    'Proxy',
    ]


class Proxy(object):
    """
    contain url handler using proxy
    """
    __slots__ = ('startUrl', 'proxyList', 'proxyCount')

    def __init__(self, startUrl = None):
        self.startUrl = startUrl
        path, file = os.path.split(configs.proxy.srcname)
        if not os.path.exists(path):
            os.makedirs(path)
        if startUrl == None:
            self.startUrl = 'http://www.baidu.com'
        if configs.proxy.rescrab:
            Logger.info('rescrab proxylist...')
            self.getFreeProxy()
        if configs.proxy.retest:
            Logger.info('retest proxy list...')
            self.testProxy()
        if not os.path.exists(configs.proxy.srcname):
            self.loadDefaultProxy()
        else:
            self.proxyList = self.loadProxy()
        self.proxyList = list(filter(lambda x:abs(int(x['available'])) == 1, self.proxyList))
        if len(self.proxyList) == 0:
            Logger.critical('There is no available proxy! espider is shuting down...')
            exit(1)
        self.proxyList.sort(key = lambda x:1000 if float(x['ping']) == -1 else float(x['ping']))
        self.proxyCount = 0


    def loadProxy(self):
        data = readLinesFile(configs.proxy.srcname)
        if data == None:
            Logger.critical('cannot load proxy list, espider is shuting down...')
            exit(1)
        proxyList = []
        for i in range(len(data)):
            proxyList.append(dict(zip(('type', 'ip', 'port', 'available', 'ping'), data[i].split('\t'))))
        return proxyList

    def getFreeProxy(self):
        """
            Two different ways getting free proxy which can be configured in configs.
            You can also define your own way of getting.
        """
        Logger.info('get free proxy from the Internet...')
        proxyList = []
        if configs.proxy.proxysrc == 1:
            for i in range(configs.proxy.srcpage):
                Logger.info('get page %s...' %(i + 1))
                req = urllib.request.Request('http://www.kuaidaili.com/free/inha/%s/' %(i + 1))
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
                data = urllib.request.urlopen(req).read().decode('utf-8')
                proxy = re.findall('<tr>\s*?<td data-title="IP">(.*?)</td>\s*?<td data-title="PORT">(.*?)</td>\s*?<td data-title="匿名度">.*?</td>\s*?<td data-title="类型">(.*?)</td>', data)
                for item in proxy:
                    if  not [item[2].lower(), item[0], item[1]] in proxyList:
                        proxyList.append([item[2].lower(), item[0], item[1]])
        if configs.proxy.proxysrc == 2:
            for i in range(configs.proxy.srcpage):
                Logger.info('get page %s...' %(i + 1))
                req = urllib.request.Request('http://www.xicidaili.com/nn/%s' %(i + 1))
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
                data = urllib.request.urlopen(req).read().decode('utf-8')
                proxy = re.findall('<td class="country"><img [\s\S]*?<td>(.*?)</td>\s*?<td>(.*?)</td>\s*?<td>[\s\S]*?</td>\s*?<td class="country">.*?</td>\s*?<td>(.*)</td>', data)
                for item in proxy:
                    if  not [item[2].lower(), item[0], item[1]] in proxyList:
                        proxyList.append([item[2].lower(), item[0], item[1]])
        dataset = []
        for item in proxyList:
            dataset.append('%s\t%s\t%s\t-1\t-1' %(item[0], item[1], item[2]))
        writeLinesFile(configs.proxy.srcname, dataset)


    def testProxy(self):
        """
            Test the proxy connection performance with self.startUrl.
        """
        req = urllib.request.Request(self.startUrl)
        for k,v in configs.urlrequest.items():
            if isinstance(v, list):
                l = len(v)
                v = v[randint(0, len(v) - 1)]
            req.add_header(k,v)
        Logger.info('test proxy list in %s' % configs.proxy.srcname)
        data = readLinesFile(configs.proxy.srcname)
        time.clock()
        proxyList = []
        for i in range(len(data)):
            proxyList.append(dict(zip(('type', 'ip', 'port'), data[i].split('\t'))))
            openner = urllib.request.build_opener(urllib.request.ProxyHandler({proxyList[i]['type']:proxyList[i]['ip'] + ':' + proxyList[i]['port']}), urllib.request.ProxyBasicAuthHandler())
            try:
                begin = time.clock()
                openner.open(req, timeout=configs.proxy.timeout)
                ping = time.clock() - begin
                available = 1
                Logger.info('proxy %s is good...' %proxyList[i]['ip'])
            except Exception as e:
                Logger.info('proxy %s is not available...' %proxyList[i]['ip'])
                ping = -1
                available = 0
            proxyList[i]['available'] = available
            proxyList[i]['ping'] = ping
        dataset = []
        for i in range(len(proxyList)):
            dataset.append('%s\t%s\t%s\t%s\t%s' %(proxyList[i]['type'], proxyList[i]['ip'], proxyList[i]['port'], proxyList[i]['available'], proxyList[i]['ping']))
        writeLinesFile(configs.proxy.srcname, dataset)
        return


    def getProxyList(self):
        return self.proxyList

    def getReqWithProxy(self, req, **kw):
        flag = False
        for i in range(len(self.proxyList)):
            try:
                proxy = self.proxyList[self.proxyCount]
                openner = urllib.request.build_opener(urllib.request.ProxyHandler({proxy['type']:proxy['ip'] + ':' + proxy['port']}), urllib.request.ProxyBasicAuthHandler())
                response = openner.open(req, **kw)
                response.read(0)
                flag = True
                if configs.proxy.mode == 2:
                    self.nextPrxoy()
                break
            except Exception:
                self.nextPrxoy()
        if flag:
            return response
        else:
            return None

    def nextPrxoy(self):
        if self.proxyCount == len(self.proxyList) - 1:
                    self.proxyCount = 0
        else:
            self.proxyCount = self.proxyCount + 1
        return


    def loadDefaultProxy(self):
        """
            If not getting proxy from web source, Proxy will use default proxy list.
        """
        self.proxyList = [{'available': '1', 'ip': '122.96.59.105', 'ping': '0.29606737168604624', 'type': 'http', 'port': '82'},
                          {'available': '1', 'ip': '111.197.129.60', 'ping': '0.38801153460738647', 'type': 'http', 'port': '8118'},
                          {'available': '1', 'ip': '119.188.94.145', 'ping': '0.5737221345580679', 'type': 'https', 'port': '80'},
                          {'available': '1', 'ip': '182.117.72.157', 'ping': '0.8478201559139222', 'type': 'http', 'port': '8118'},
                          {'available': '1', 'ip': '180.107.228.186', 'ping': '1.0205159783961264', 'type': 'http', 'port': '808'},
                          {'available': '1', 'ip': '119.6.136.122', 'ping': '1.377177670300096', 'type': 'http', 'port': '80'},
                          {'available': '1', 'ip': '203.195.152.95', 'ping': '1.4270706915205267', 'type': 'http', 'port': '80'},
                          {'available': '1', 'ip': '223.11.253.114', 'ping': '1.7851766325845517', 'type': 'http', 'port': '80'},
                          {'available': '1', 'ip': '39.87.117.22', 'ping': '1.8674158744820346', 'type': 'http', 'port': '8118'},
                          {'available': '1', 'ip': '123.59.35.169', 'ping': '2.576883175751668', 'type': 'http', 'port': '80'},
                          {'available': '1', 'ip': '117.87.136.5', 'ping': '3.3327759888588133', 'type': 'http', 'port': '8118'}]
        dataset = []
        for item in self.proxyList:
            dataset.append('%s\t%s\t%s\t%s\t%s' %(item['type'], item['ip'], item['port'], item['available'], item['ping']))
        writeLinesFile(configs.proxy.srcname, dataset)