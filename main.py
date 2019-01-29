#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from warranty import CheckWarranty

def main():
    proxies = {'http':'http://proxy.standard.corp:8080','https':'http://proxy.standard.corp:8080'}
    user = input("请输入代理服务器用户名（一般是ls\\xxx格式）：")
    password = input("请输入代理服务器密码：")
    userpass = user+':'+password   

    warranty = CheckWarranty(proxies,userpass)
    with open('sn.txt','r') as f:
        sn = f.readlines()
    sn = [i.strip() for i in sn]

    hpsn = []
    lxsn = []
    for i in sn:
        if len(i) == 10:
            hpsn.append(i)
        else:
            lxsn.append(i)
    
    print('------需查询HP序列号%s个，联想序列号%s个' % (len(hpsn),len(lxsn)))
    print('------下面开始查询HP序列号，20个一组，耐心等待')
    for i in range(0,len(hpsn),20):
        temp = hpsn[i:i+20]
        time.sleep(5)
        warranty.hp(*temp)

    print('------下面开始查询联想序列号')
    for m in lxsn:
        warranty.lenovo(m)

main()
