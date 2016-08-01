#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test/lianjia
    ------------------------------------------------------------

    This file is an example which scrab www.lianjia.com

"""

__author__ = 'MeteorKepler'

import re
from bs4 import BeautifulSoup

from espider.spider import BaseSpider
from espider.parser import HtmlParser

class LianjiaSpider(BaseSpider):

    espiderName = 'LianjiaSpider'

    def __init__(self):
        startUrl = 'http://bj.lianjia.com/xiaoqu/'
        super(LianjiaSpider, self).__init__(startUrl)

    def getUrlList(self, response):
        data = response.read().decode('utf8')
        beso = BeautifulSoup(data, 'html.parser')
        tags = beso.body.find('div', class_ = 'position').find_all('a', href = re.compile('/.+?/.+?/'))
        catalogueUrllist = []
        for item in tags:
            catalogueUrllist.append(item['href'])
        tag = beso.find('div', class_ = 'page-box house-lst-page-box')
        if tag !=None:
            pageurl = tag['page-url']
            pagedata = eval(tag['page-data'])
            for i in range(pagedata['totalPage']):
                catalogueUrllist.append(pageurl.replace('{page}', '%s' %(i + 1)))
        contentUrllist = re.findall('<div class="title"><a href="(.*?)"', data)

        return (catalogueUrllist, contentUrllist)

class LianjiaParser(HtmlParser):
    def parseContent(self, data):
        dataList = []
        primaryKey = 'name'
        item = {}
        item['name'] = re.findall('<h1 class="detailTitle">(.*?)</h1>', data)[0]
        item['price'] = re.findall('<span class="xiaoquUnitPrice">(.*?)</span>', data)[0]
        dataList.append(item)
        return dataList

myEspider = LianjiaSpider()
myEspider.startEspider()

myParser = LianjiaParser(primaryKey='name')
myParser.startParseContent()