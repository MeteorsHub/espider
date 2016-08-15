#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test/NationalGeographic
    ------------------------------------------------------------

    This file is an example which scrab www.nationalgeographic.com

"""

__author__ = 'MeteorKepler'

import re

from espider.spider import BaseSpider

class NationalGeo(BaseSpider):
    espiderName = 'nationalGeographicSpider'
    startUrl = 'http://ocean.nationalgeographic.com/ocean/photos/underwater-exploration-photos/'

    def getUrlList(self, response):
        data = response.read().decode('utf8')
        cataloguelist = re.findall('''<a href="(/ocean/.*?)" title=".*?">.*?</a>''', data)
        contentList = re.findall('''<a class="thumb" title=".*?" href='(.*?)'>''', data)
        return (cataloguelist, contentList)

from espider.config import configs
configs.spider.catalogueLimit = 5
configs.spider.contentLimit = 20

mySpider = NationalGeo()
mySpider.startEspider()
