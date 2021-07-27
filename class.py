# -*- coding: utf-8 -*-
import os
import datetime
import logging
from flask import render_template


def abcd(x: int):
    print(x)


class Test(object):
    def __init__(self):
        second = 'I will created after the one'
    one = 'I will created before the second'

    def instancefun(self):  # 实例方法
        print('instancefun')
        print(self)

    @classmethod  # 类方法
    def classfun(cls):
        print('classfun')
        print(cls)

    @staticmethod  # 静态方法
    def staticfun():
        print('staticfun')

    def function(self):  # 普通函数
        print('func')


abcd(x='abc')

obj_t = Test()
# obj_t.instancefun
obj_t.instancefun()  # 对象调用实例方法
# obj_t.function  # 对象不能调用函数？
obj_t.staticfun()  # 静态方法
obj_t.classfun()  # 类方法
# print '---------------------------------------'
Test.instancefun(obj_t)
# Test.instancefun(Test)
# Test.function()
Test.staticfun()
Test.classfun()

import json


def send_email2(to_list, subject, content, template, files, **kwargs):
    from smtplib import SMTP_SSL
    from email.header import Header
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    to_list = ['xtet2008@126.com'] if not to_list else to_list
    to_list = [to_list] if not isinstance(to_list, list) else to_list

    mail_info = {
        "from": "370726390@qq.com",
        "to": to_list,
        "hostname": "smtp.qq.com",
        "username": "370726390@qq.com",
        "password": "sdfbcdgqmbjwbjca",
        "mail_subject": subject,
        "mail_text": content,
        "mail_encoding": "utf-8"
    }

    smtp = SMTP_SSL(mail_info.get('hostname'))
    smtp.set_debuglevel(0)  # 1 will be print mail send msg log , 0 hiden the mail send log
    smtp.ehlo(mail_info.get('hostname'))
    smtp.login(mail_info.get('username'), mail_info.get('password'))

    msg = MIMEMultipart()
    msg['Subject'] = Header(mail_info.get('mail_subject'), mail_info.get('mail_encoding'))
    msg['From'] = mail_info.get('from')
    msg['To'] = ';'.join(to_list)
    if mail_info.get('mail_text'):
        msg.attach(MIMEText(mail_info.get('mail_text'), _subtype='plain', _charset=mail_info.get('mail_encoding')))
    if template:
        subtype = 'html' if os.path.splitext(template)[1] == '.html' else 'plain'
        msg.attach(MIMEText(render_template(template, **kwargs), _subtype=subtype, _charset='utf-8'))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            part.set_charset('utf-8')
            msg.attach(part)

    try:
        smtp.sendmail(mail_info.get('from'), mail_info.get('to'), msg.as_string())
    except Exception as e:
        print
        e
        print
        e.message
        return False
    finally:
        smtp.quit()
    return True


result = "email content"
send_email2(to_list=None, subject='inventory-input args', content=json.dumps(result), template=None, files=None)