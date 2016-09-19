#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utility as util
import netifaces as ni

if "__main__" == __name__:
    conf = util.config('../info.conf').get_dict()
    from_addr = conf['email']['email_addr']
    password = conf['email']['email_pd']
    smtp_server = conf['email']['smtp_server']
    smtp_port = conf['email']['smtp_port']
    to_addr = 'stkky@sina.com'

    lan_ip = ni.ifaddresses('eth0')[2][0]['addr'] if 2 in ni.ifaddresses('eth0') else 'don\'t connect lan'
    wifi_ip = ni.ifaddresses('wlan0')[2][0]['addr'] if 2 in ni.ifaddresses('wlan0') else 'don\'t connect wifi'
    public_ip = util.get_public_ip()
    content = '公网IP为: %s\r\n有线网卡IP为: %s\r\n无线网卡IP为: %s\r\n' % (public_ip, lan_ip, wifi_ip)
    print content
    util.sent_email(content, from_addr, u'raspberrypi', password, smtp_server, smtp_port, to_addr, u'田琨', u'Raspberry IP')


