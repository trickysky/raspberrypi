#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/6/19

from flask import Flask, request
from EmailService import Email
app = Flask(__name__)

@app.route("/s/ip_report", methods=['POST'])
def hello():
    name = request.form['name']
    ipv4 = request.form['ipv4']
    ipv6 = request.form['ipv6']
    theme = '[IP Report] %s' % name
    content = 'IPV4: %s \nIPV6: %s' % (ipv4, ipv6)
    if Email().sent_email(theme, content, 'iam@tiankun.me', 'iam@tiankun.me'):
        return '%s IP report complete: %s; %s' % (name, ipv4, ipv6)
    else:
        return '%s IP report error'

if __name__ == '__main__':
    app.run(host='::')