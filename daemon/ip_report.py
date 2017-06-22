#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/6/19

import os, requests

if '__main__' == __name__:
    url = 'http://ipv6.vultr.tiankun.me:5000/s/ip_report'

    ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
    ipv6 = os.popen('ip addr show eth0').read().split("inet6 ")[1].split("/")[0]
    data = {
        'name': 'pi',
        'ipv4': ipv4,
        'ipv6': ipv6,
    }
    requests.post(url=url, data=data)