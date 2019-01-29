#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from req import session

class CheckWarranty(object):
    def __init__(self,proxies={},userpass=''):
        self.proxies = proxies
        self.userpass = userpass

    def hp(self,*args):
        
        ssid_url = 'https://support.hp.com/cn-zh/checkwarranty/multipleproducts'
        api_url = 'https://support.hp.com/hp-pps-services/os/multiWarranty?ssid='
        sup_url = 'https://support.hp.com'
        payload = {"gRecaptchaResponse":"","obligationServiceRequests":[]}
        for sn in args:
            payload['obligationServiceRequests'].append({"serialNumber":sn,"isoCountryCde":"CN","lc":"ZH","cc":"CN","modelNumber":""})
        payload_json = json.dumps(payload)
        ssid_re = re.compile(r'.*mwsid":"(.*)".*')
        r = session(self.proxies,self.userpass)
        #r = session()

        #请求ssid url
        body = r.get(ssid_url)
        #组合第二次请求的url
        ssid = re.findall(ssid_re,body)[0]
        api_url = api_url + ssid
        #第二次请求url
        result = json.loads(r.post(api_url,payload_json,'json'))
        #print(result)

        #r_hp = {}
        for i in result['productWarrantyDetailsVO']:
        #    r_hp[i['serialNumber']] = [i['warrantyResultList'][0]['obligationStartDate'],i['warrantyResultList'][0]['obligationEndDate'],sup_url+i['warrantyResultRedirectUrl']]
            print(i['serialNumber'],i['warrantyResultList'][0]['obligationStartDate'],i['warrantyResultList'][0]['obligationEndDate'])

    def lenovo(self,sn):
        api_url = 'https://ibase.lenovo.com/POIRequest.aspx'

        re_startData = re.compile(r'.*<warstart>(.*)</warstart>.*')
        re_endData = re.compile(r'.*<wed>(.*)</wed>.*')
        re_serial = re.compile(r'.*<serial>(.*)</serial>.*')
        payload = "xml=<wiInputForm source='ibase'> \
                <id>LSC3</id> \
                <pw>IBA4LSC3</pw> \
                <product></product> \
                <serial>%s</serial> \
                <wiOptions><machine/> \
                <parts/><service/><upma/> \
                <entitle/></wiOptions> \
                </wiInputForm>" % sn
        r = session(self.proxies,self.userpass)

        result = r.post(api_url,payload,'xml')
        print(re_serial.findall(result)[0],re_startData.findall(result)[0],re_endData.findall(result)[0])

if __name__ == '__main__':
    pass
