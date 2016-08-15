#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test/NationalGeographic
    ------------------------------------------------------------

    This file is an example which scrab www.nationalgeographic.com

"""

__author__ = 'MeteorKepler'



from espider.spider import BaseSpider

class YinyuetaiSpider(BaseSpider):
    espiderName = 'YinyuetaiSpider'
    startUrl = 'http://news.yinyuetai.com/type/neidi'


    def getUrlList(self, response):
        data = response.read().decode('utf8')
        catalogueList = re.find