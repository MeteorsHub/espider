#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.http
    ------------------------------------------------------------

    This file is about http request and response handler

"""

__author__ = 'MeterKepler'

import urllib.error
import urllib.request
from urllib.parse import urlparse

from espider.proxy import Proxy
from espider.log import *



class HttpHandler(object):
    host = None
    proxy = None
    selephan = None

    def __init__(self, host = None):
        self.host = host
        if config.configs.http.proxy:
            self.proxy = Proxy(host)
        if config.configs.http.selephan:
            from espider.selephan import SelePhan
            self.selephan = SelePhan(self.proxy)

    def getResponseByUrl(self, url, headers={}):
        if urlparse(url).hostname == None:
            Logger.error('url of request illegal! which is %s' %url)
            return None
        req = urllib.request.Request(url)
        for k,v in config.configs.urlrequest.items():
            req.add_header(k,v)
        for k,v in headers.items():
            req.add_header(k,v)
        flag = False
        for i in range(config.configs.http.retry):
            try:
                if self.selephan != None:
                    response = self.selephan.getReqWithSel(req)
                    if response == None:
                        continue
                    else:
                        flag = True
                        break
                if self.proxy != None:
                    response= self.proxy.getReqWithProxy(req, timeout=config.configs.proxy.timeout)
                    if response == None:
                        continue
                    else:
                        flag = True
                        break
                response = urllib.request.urlopen(req, timeout=config.configs.http.timeout)
                flag = True
                break
            except Exception as e:
                continue
        if flag:
            return response
        else:
            return None

    def nextHandler(self):
        if config.configs.http.selephan:
            self.selephan.nextProxy()
        if config.configs.http.proxy:
            self.proxy.nextPrxoy()
        return