#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test/lianjia
    ------------------------------------------------------------

    This file is an example which scrab www.nationalgeographic.com

"""

__author__ = 'MeteorKepler'

import re

from espider.spider import BaseSpider

class NationalGeo(BaseSpider):
    def __init__(self, startUrl):
        return super().__init__(startUrl)

    def getUrlList(self, response):
        data = response.read().decode('utf8')
        contentList = re.findall('''<a class="thumb" title=".*?" href='(.*?)'>''', data)
