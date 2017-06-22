#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/2/14

import config


class Email(object):
    def __init__(self, smtp_server=config.TECENT_EMAIL['server'], smtp_port=config.TECENT_EMAIL['port'],
                 user_name=config.TECENT_EMAIL['username'], password=config.TECENT_EMAIL['password']):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user_name = user_name
        self.password = password

    def sent_email(self, theme, content, sender, receiver):
        from email.header import Header
        from email.mime.text import MIMEText
        from email.utils import parseaddr, formataddr
        import smtplib

        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr(
                (Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = _format_addr(u'%s <%s>' % (None, sender))
            msg['To'] = _format_addr(u'%s <%s>' % (None, receiver))
            msg['Subject'] = Header(u'%s' % theme, 'utf-8').encode()

            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)
            server.login(self.user_name, self.password)
            server.sendmail(self.user_name, [receiver], msg.as_string())
            server.quit()
            return 1
        except Exception, e:
            print 'sent email error: %s' % e
            return 0


if '__main__' == __name__:
    a = Email()
    a.sent_email('test', 'test', 'iam@tiankun.me', 'iam@tiankun.me')
