from urllib.parse import urlparse
import time, hashlib, base64

class authorizationDecoder(object):

    def __init__(self, url):
        self.url = url
        self.app_id = '20160106_android'
        self.app_secret = '06fc5d7d1572a8ee14ba2145315f676b'
        
        self.url = url + '&request_ts=' + self.getTs()
        self.queryString = urlparse(self.url).query
        self.queryString = self.app_secret + self.queryString.replace('&', '')
        self.str2 = self.decodeStr2()
        self.str3 = self.app_id + ':' + self.str2
        self.str1 = base64.b64encode(self.str3.encode('utf8')).decode('utf8')



    def getTs(self):
        ts = '%s' %int(time.time())
        return ts

    def decodeStr2(self):
        has = hashlib.sha1(self.queryString.encode('utf8')).hexdigest()
        return has

    def getUrl(self):
        return self.url

    def getHeaders(self):
        headers = {}
        headers['Authorization'] = self.str1
        return headers