#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
import sys

logging.basicConfig(filename='%s/.log' % sys.path[0], level=logging.INFO)


# 读取配置文件
class config(object):
    def __init__(self):
        from pathlib import Path
        self.path = '%s/info.conf' % os.path.dirname(os.path.abspath(__file__))

    def read(self):
        import ConfigParser
        import os
        parser = ConfigParser.ConfigParser()
        if os.path.isfile(self.path):
            parser.read(self.path)
            return parser
        else:
            logging.error('can\'t find info.conf: %s' % self.path)

    def get_dict(self):
        parser = self.read()
        config_dict = {}
        for section in parser.sections():
            config_dict[section] = {}
            for option in parser.options(section):
                config_dict[section][option] = parser.get(section, option)
        return config_dict

    def get_sections(self):
        parser = self.read()
        return parser.sections()


# 获取当前的公网IP
def get_public_ip():
    import urllib2
    url = 'http://ip.cip.cc/'
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().strip()
    except Exception, e:
        logging.error('get public ip error: %s' % e)
        return 0


class network(object):
    def __init__(self, name):
        self.name = name

    def is_connect(self):
        import netifaces as ni
        return True if 2 in ni.ifaddresses(self.name) else False

    def get_ip(self):
        import netifaces as ni
        return ni.ifaddresses(self.name)[2][0]['addr'] if self.is_connect() else 'no %s' % self.name

    def get_ssid(self):
        if not self.is_connect():
            return 'no %s' % self.name
        else:
            from subprocess import check_output
            scanoutput = check_output(["iwconfig", self.name])
            ssid = "ssid not found"
            for line in scanoutput.split():
                line = line.decode("utf-8")
                if "ESSID" in line:
                    ssid = line.split('"')[1]
            return ssid


# 发送email
def sent_email(content, from_addr, from_name, password, smtp_server, smtp_port, to_addr, to_name, theme):
    from email.header import Header
    from email.mime.text import MIMEText
    from email.utils import parseaddr, formataddr
    import smtplib

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr(u'%s <%s>' % (from_name, from_addr))
        msg['To'] = _format_addr(u'%s <%s>' % (to_name, to_addr))
        msg['Subject'] = Header(u'%s' % theme, 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except Exception, e:
        logging.error('sent email error: %s' % e)


# Return CPU temperature as a character string
def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def get_ram_info():
    p = os.popen('free -h')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


# Return % of CPU used by user as a character string
def get_cpu_percent():
    import psutil
    return psutil.cpu_percent()


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])


class AliyunMonitor:
    def __init__(self, url):
        conf = config().get_dict()
        self.access_id = conf['ali']['access_key_id']
        self.access_secret = conf['ali']['access_key_secret']
        self.url = url

    # 签名
    def sign(self, accessKeySecret, parameters):
        import hmac
        import base64
        from hashlib import sha1
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])    # 使用get请求方法
        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        import urllib
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        import time
        import uuid
        import urllib
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'JSON',
            'Version': '2015-01-09',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature

        # return parameters
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url