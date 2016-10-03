#!/usr/bin/python
# -*- coding: UTF-8 -*-
# trickysky

import utility

if '__main__' == __name__:
    aliyun = utility.AliyunMonitor("http://alidns.aliyuncs.com")
    payload = {
        'Action': 'DescribeDomainRecords',
        'DomainName': 'tiankun.me'
    }
    url = aliyun.make_url(payload)
    print url
    # import urllib2
    # request = urllib2.Request(url)
    # response = urllib2.urlopen(request)
    # print response.read().strip()
