#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.test_lianjia_json.lianjiajson
    ------------------------------------------------------------

    This file is an example which scrab json data from www.lianjia.com

"""

__author__ = 'MeteorKepler'

import json
from collections import OrderedDict

from espider.spider import UrlQuerySpider
from espider.util import json_get

class myLianjiaJsonSpider(UrlQuerySpider):
    startUrl = 'https://moapi.lianjia.com/house/house/'
    queryList = ['getbuildings', 'getUnits', 'getHouses']
    parameterList = ['community_id', 'building_id', 'unit_id']
    extraParameter = OrderedDict([('app_id', 'siren'), ('app_secret', '195e882bdf0e61bce64cad045d704b8c')])

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


mySpider = myLianjiaJsonSpider()
mySpider.startEspider()
