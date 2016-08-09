#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.mysql
    ------------------------------------------------------------

    This file is about operating mysql database.
    It provide basic operation of sql including 'CREATE TABLE', 'SELECT' and 
    an additional function about INSERT with UPDATE.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import pymysql
import warnings
warnings.filterwarnings("ignore")

from espider.config import configs
from espider.log import Logger

__all__ = [
    'Mysql',
    ]

class Mysql(object):

    """
        This class will use configs to create a connection to mysql.
        Providing basic operations including 'CREATE TABLE', 'SELECT' and 
        an additional function about INSERT with UPDATE which will automatically 
        judge whether the tuple is already in database and update it if so.
    """

    def __init__(self, table, keyList, primaryKey = None):
        self.table = table
        self.keyList = keyList
        self.primaryKey = primaryKey
        if self.primaryKey != None:
            if self.primaryKey in self.keyList:
                index = self.keyList.index(self.primaryKey)
                self.keyList[0], self.keyList[index] = self.keyList[index], self.keyList[0]

        self.createTable()

    def select(self,selectKeyList = None):
        temp = []
        if selectKeyList == None:
            temp = '*'
        else:
            if not isinstance(selectKeyList, list):
                Logger.error('selectKeyList error because it is not a list...')
                return None
            temp = ','.join(selectKeyList)
        sql = 'SELECT %s FROM %s' %(temp, self.table)
        result = list(self.__sqlExecute(sql))
        if selectKeyList == None:
            sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" %(self.table, configs.mysql.db)
            selectKeyList = list(self.__sqlExecute(sql))
            for i in range(len(selectKeyList)):
                selectKeyList[i] = selectKeyList[i][0]
        ret = []
        for item in result:
            ret.append(dict(zip(selectKeyList, item)))
        return ret

    def createTable(self):
        if not isinstance(self.keyList, list):
            Logger.error('key list error when creating table %s' %self.table)
            return
        if len(self.keyList) == 0:
            Logger.error('key list without an element in it, cannot create table %s' %self.table)
            return
        keyList = list()
        for i in range(len(self.keyList)):
            keyList.append(self.keyList[i] + ' VARCHAR(255)')
        if self.primaryKey != None:
            if self.primaryKey == self.keyList[0]:
                keyList[0] = keyList[0] + ' PRIMARY KEY'
        temp = ','.join(keyList)
        sql = "CREATE TABLE IF NOT EXISTS %s(%s)" %(self.table, temp)
        self.__sqlExecute(sql)
        return

    def insertWithUpdate(self, insertList):
        if not isinstance(insertList, list):
            Logger.error('insert list error because it is not a list...')
        if len(insertList) == 0:
            return
        keyList = []
        for k in insertList[0]:
            keyList.append(k)
        if not self.checkKeyList(keyList):
            return
        temp1 = ','.join(self.keyList)
        for item in insertList:
            valueList = []
            for k in self.keyList:
                valueList.append("'" + item[k] + "'")
            temp2 = ','.join(valueList)
            keyValueList = []
            for i in range(1, len(self.keyList)):
                keyValueList.append(self.keyList[i] + '=' + "VALUES(" + self.keyList[i] + ")")
            temp3 = ','.join(keyValueList)
            sql = "INSERT INTO %s(%s)VALUES(%s)ON DUPLICATE KEY UPDATE %s" %(self.table, temp1, temp2, temp3)
            self.__sqlExecute(sql)

    def __sqlExecute(self,sql):
        data = None
        try:
            connection = pymysql.connect(host = configs.mysql.host, port = configs.mysql.port, user = configs.mysql.user, password = configs.mysql.password, db = configs.mysql.db, charset = 'utf8')
            try:
                with connection.cursor() as cur:
                    cur.execute(sql)
                    data = cur.fetchall()
                    connection.commit()
            except Exception:
                Logger.error('sql statement execute error:%s' %sql)
            finally:
                connection.close()
        except Exception:
            Logger.error('mysql database open with error...')
        return data

    def checkKeyList(self, keyList):
        flag = True
        if len(self.keyList) != len(keyList):
            Logger.error('keyList length do not match...')
            return False
        for item in keyList:
            if item not in self.keyList:
                Logger.error('keyList element do not match')
                flag = False
                break
        return flag