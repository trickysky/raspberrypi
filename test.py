#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/6/14

import os, requests

if '__main__' == __name__:
    ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
    ipv6 = os.popen('ip addr show eth0').read().split("inet6 ")[1].split("/")[0]
    url= 'http://ipv6.vultr.tiankun.me:5000'
    r = requests.get(url)
    print ipv4
    print ipv6
    print r.text
