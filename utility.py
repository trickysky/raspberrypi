#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
logging.basicConfig(filename='%s/.log' % os.path.abspath('.'), level=logging.INFO)

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

