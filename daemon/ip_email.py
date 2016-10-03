#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utility as util
import netifaces as ni
import time, datetime, sys

retry_times_max = 6

if "__main__" == __name__:
    conf = util.config().get_dict()
    from_addr = conf['email']['email_addr']
    password = conf['email']['email_pd']
    smtp_server = conf['email']['smtp_server']
    smtp_port = conf['email']['smtp_port']
    to_addr = 'stkky@sina.com'
    path = sys.path.append(1)

    retry_times = 0
    while retry_times < retry_times_max:
        if 2 in ni.ifaddresses('eth0') or 2 in ni.ifaddresses('wlan0'):
            lan_ip = ni.ifaddresses('eth0')[2][0]['addr'] if 2 in ni.ifaddresses('eth0') else 'don\'t connect lan'
            wifi_ip = ni.ifaddresses('wlan0')[2][0]['addr'] if 2 in ni.ifaddresses('wlan0') else 'don\'t connect wifi'
            public_ip = util.get_public_ip()
            content = u'时间: %s\r\n' % datetime.datetime.now()
            content += u'公网IP为: %s\r\n有线网卡IP为: %s\r\n无线网卡IP为: %s\r\n' % (public_ip, lan_ip, wifi_ip)
            util.sent_email(content, from_addr, u'raspberrypi', password, smtp_server, smtp_port, to_addr, u'田琨', u'Raspberry IP')
            break
        else:
            retry_times += 1
            time.sleep(10)

