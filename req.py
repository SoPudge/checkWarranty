#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import certifi
from io import BytesIO 
from io import StringIO 
from urllib.parse import urlencode, quote_plus

class session(object):
    def __init__(self,proxies={},userpass=''):

        self.c = pycurl.Curl()
        #if no proxy,send data directly,or via proxy
        if len(proxies) != 0:
            self.c.setopt(self.c.PROXY, proxies['http'])
            self.c.setopt(self.c.PROXYUSERPWD, userpass)
            self.c.setopt(self.c.PROXYAUTH, self.c.HTTPAUTH_NTLM)
            self.c.setopt(self.c.CAINFO, certifi.where())
        self.c.setopt(self.c.VERBOSE,0)
        self.c.setopt(self.c.COOKIEJAR, 'cookie.txt')
        self.c.setopt(self.c.COOKIEFILE, 'cookie.txt')

    def get(self,url):
        '''
        '''
        buffers = BytesIO()
        self.c.setopt(self.c.URL,url)
        self.c.setopt(self.c.WRITEDATA, buffers)
        self.c.perform()
        return buffers.getvalue().decode()

    def post(self,url,payload,ctype=''):
        '''
        '''
        buffers = BytesIO()
        self.c.setopt(self.c.URL,url)
        self.c.setopt(self.c.WRITEDATA, buffers)
        if ctype == 'json':
            self.c.setopt(self.c.HTTPHEADER,['Content-Type: application/json; charset=utf-8'])
        elif ctype == 'xml':
            self.c.setopt(self.c.HTTPHEADER,['Content-Type: application/x-www-form-urlencoded; charset=utf-8'])
        else:
            self.c.setopt(self.c.HTTPHEADER,['Content-Type: application/x-www-form-urlencoded; charset=utf-8'])
            payload = urlencode(payload, quote_via=quote_plus)
        self.c.setopt(self.c.POSTFIELDS, payload)
        self.c.perform()
        return buffers.getvalue().decode()

if __name__ == '__main__':
    pass
