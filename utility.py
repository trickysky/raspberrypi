#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import sys

logging.basicConfig(filename='%s/.log' % sys.path[0], level=logging.INFO)


# 读取配置文件
class config(object):
    def __init__(self, path):
        self.path = path

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
            scanoutput = check_output(["iwconfig"])
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
