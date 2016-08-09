#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.http
    ------------------------------------------------------------

    This module is a http request and response handler.
    It uses different method to manipulate http connections, including send 
    directly, via proxy and using selenium and phantomjs.
    If you use selephon to load website dynamicly, you should build environment 
    according to instructions in README.md.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import urllib.error
import urllib.request
from urllib.parse import urlparse

from espider.proxy import Proxy
from espider.config import configs
from espider.log import Logger

__all__ = [
    'HttpHandler',
    ]

class HttpHandler(object):
    """
        Sustain web request module.
        Provide function using next way contact with server.
        Contain request settings.
    """

    host = None
    # Whether using proxy
    proxy = None
    # Whether using selephan
    selephan = None

    def __init__(self, host = None):
        self.host = host
        if configs.http.proxy:
            self.proxy = Proxy(host)
        if configs.http.selephan:
            from espider.selephan import SelePhan
            self.selephan = SelePhan(self.proxy)

    def getResponseByUrl(self, url, headers={}):
        """
            url is the website you want.
            headers is the dict you add dynamicly apart from that in configs
        """
        if urlparse(url).hostname == None:
            Logger.error('url of request illegal! which is %s' %url)
            return None
        req = urllib.request.Request(url)
        for k,v in configs.urlrequest.items():
            req.add_header(k,v)
        for k,v in headers.items():
            req.add_header(k,v)
        flag = False
        for i in range(configs.http.retry):
            try:
                if self.selephan != None:
                    response = self.selephan.getReqWithSel(req)
                    if response == None:
                        continue
                    else:
                        flag = True
                        break
                if self.proxy != None:
                    response= self.proxy.getReqWithProxy(req, timeout=configs.proxy.timeout)
                    if response == None:
                        continue
                    else:
                        flag = True
                        break
                response = urllib.request.urlopen(req, timeout=configs.http.timeout)
                flag = True
                break
            except Exception as e:
                continue
        if flag:
            return response
        else:
            return None

    def nextHandler(self):
        """
            If the connection fails, use this function to try another time.
        """
        if configs.http.selephan:
            self.selephan.nextProxy()
        if configs.http.proxy:
            self.proxy.nextPrxoy()
        return