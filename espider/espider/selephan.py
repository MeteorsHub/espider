#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.selephan
    ------------------------------------------------------------

    This file is about use selenium and phantomJs to handle web page.
    If your page is generated in JavaScript, this method will help you.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""
from random import randint

__author__ = 'MeterKepler'

import urllib.request
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy as seleProxy
from selenium.webdriver.common.proxy import ProxyType

from espider.proxy import *
from espider.config import configs
from espider.log import Logger

__all__ = [
    'SelePhan',
    'PhantomJsResponse',
    ]


class SelePhan(object):
    proxy = None
    proxyList = []
    proxyCount = 0
    cap = webdriver.DesiredCapabilities.PHANTOMJS

    def __init__(self, esProxy = None):
        if esProxy != None:
            self.proxyList = esProxy.getProxyList()
            self.proxyCount = 0
        self.formProxy(self.proxyCount)
        self.cap['phantomjs.page.settings.resourceTimeout'] = configs.selephan.timeout*1000
        self.cap['phantomjs.page.settings.loadImages'] = configs.selephan.loadimages
        if isinstance(configs.urlrequest['User-Agent'], list):
            userAgent = configs.urlrequest['User-Agent'][randint(0, len(configs.urlrequest['User-Agent']) - 1)]
        self.cap['phantomjs.page.settings.userAgent'] = configs.urlrequest['User-Agent']
        self.driver = webdriver.PhantomJS(desired_capabilities=self.cap, proxy=self.proxy)


    def getReqWithSel(self, request):
        if not isinstance(request, urllib.request.Request):
            Logger.error('SelePhan request error: please make sure request is a urllib.request.Request object...')
            return None
        url = request.full_url
        self.driver.get(url)
        response = PhantomJsResponse(self.driver.page_source, {'Content-Type':'text/html'})
        return response

    def formProxy(self, count):
        if len(self.proxyList) == 0:
            self.proxy = None
            return
        if count >= len(self.proxyList):
            Logger.error('SelePhan proxy form error:out of range in proxyList...')
            self.proxy = None
            return
        proxy = self.proxyList[count]
        ipport = proxy['ip'] + ':' + proxy['port']
        proxyDict = {'proxyType':ProxyType.MANUAL}
        if proxy['type'] == 'http':
            proxyDict['httpProxy'] = ipport
        elif proxy['type'] == 'socks':
            proxyDict['socksProxy'] = ipport
        else:
            self.proxy = None
            return
        self.proxy = seleProxy(proxyDict)
        return

    def nextProxy(self):
        if self.proxy == None:
            return
        if self.proxyCount >=len(self.proxyList):
            self.proxyCount = 0
        else:
            self.proxyCount = self.proxyCount + 1
        self.formProxy(self.proxyCount)
        self.driver = webdriver.PhantomJS(proxy=self.proxy)

class PhantomJsResponse(object):
    data = b''
    headers = {}

    def __init__(self, data = '', headers = {}):
        self.data = bytes('' ,encoding='utf8')
        self.headers = {}
        self.setData(data)
        self.setHeaders(headers)

    def setData(self, data):
        if not isinstance(data, str):
            Logger.error('PhantomJsResponse setData() error: data is not a str...')
            return
        self.data = bytes(data, encoding='utf8')

    def setHeaders(self, headers):
        if not isinstance(headers, dict):
            Logger.error('PhantomJsResponse setHeaders() error: headers is not a dict...')
            return
        self.headers = headers

    def getheader(self, header):
        if not isinstance(header, str):
            return None
        if header in self.headers:
            return self.headers[header]
        return None

    def getheaders(self):
        if len(self.headers) == 0:
            return None
        return self.headers

    def read(self):
        return self.data


