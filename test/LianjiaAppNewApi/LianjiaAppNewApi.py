#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test/LianjiaAppNewApi
    ------------------------------------------------------------

    This file is an example which uses espider.spider.UrlQuerySpider to scribe data dict via Lianjia Android app's new api.
    In the latest lianjia app, we found it generate an Authorization code to communicate with lianjia server whoes domain is 
    https://app.api.lianjia.com/yezhu/publish/. So we crack the generation method from the app and emulate it to get data dict. 

    Our goal is to study crawling technology and anyone's using for commercial or improper purpose is denied.

"""

__author__ = 'MeteorKepler'


from collections import OrderedDict
import json

from espider.spider import UrlQuerySpider
from decode import authorizationDecoder
from espider.util import json_get

class myLianjiaNewSpider(UrlQuerySpider):
    startUrl = 'https://app.api.lianjia.com/yezhu/publish/'
    queryList = ['getbuildings', 'getUnits', 'getHouses']
    parameterList = ['community_id', 'building_id', 'unit_id']
    extraParameter = OrderedDict([('app_id', '20160106_android'), ('app_secret', '7a01588bac315706bbad9beac5136cd647c1ae25')])


    def contentHandler(self, data):
        data = json.loads(data)
        ret = []
        buidingList = json_get(data, 'building_id')
        if buidingList != None:
            if len(buidingList) != 0:
                for item in buidingList:
                    temp = {}
                    temp['building_id'] = item
                    ret.append(temp)
        unitList = json_get(data, 'unit_id')
        if unitList != None:
            if len(unitList) != 0:
                for item in unitList:
                    temp = {}
                    temp['unit_id'] = item
                    ret.append(temp)
        return ret

    def buildExtraHeaders(self, url):
        auDe = authorizationDecoder(url)
        url1 = auDe.getUrl()
        headers = auDe.getHeaders()
        return (url1, headers)



mySpider = myLianjiaNewSpider()
mySpider.startEspider()