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

class YinyuetaiSpider(BaseSpider):
    espiderName = 'YinyuetaiSpider'
    startUrl = 'http://news.yinyuetai.com/type/neidi'


    def getUrlList(self, response):
        data = response.read().decode('utf8')
        catalogueList = re.findall('<a href="(.*?)"\s*?onclick=".*?"\s*?class="nextpage">', data)
        contentList = re.findall('<a href="(/article/.*?)" class="in_article_pic" title=".*?" target=".*?">', data)
        contentList = list(set(contentList))
        return (catalogueList, contentList)

    def contentAvailable(self, response):
        data = response.read().decode('utf8')
        if re.findall('<title>(.*?)</title>', data) == []:
            return False
        return True

    def contentFileName(self, response):
        name = re.findall('<title>(.*?)</title>', response.read().decode('utf8'))[0]
        return name + '.html'

mySpider = YinyuetaiSpider()
mySpider.startEspider()