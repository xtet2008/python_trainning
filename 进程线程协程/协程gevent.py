#!/usr/bin/env python
# encoding: utf-8
"""
@Author: ZhangSheng
@Contact: xtet2008@126.com
@File: 协程gevent.py
@Time: 2018/9/28 0028 下午 13:53
@Software: PyCharm
@Desc:
"""

import gevent
import threading
from gevent import monkey
from urllib import request
monkey.patch_all()


def get_body(url):
    print('Visit --> %s' % url)
    try:
        response = request.urlopen(url)
        data = response.read()
        print("%d bytes received from %s." % (len(data), url))
    except Exception:
        print("error")


urls = ['https://github.com/', 'https://blog.csdn.net/', 'https://bbs.csdn.net/', 'http://www.baidu.com',
        "https://www.google.com.hk", "https://zhuanlan.zhihu.com/p/189993070"
        ]

tasks = [gevent.spawn(get_body, url) for url in urls]
# print (tasks)
print('testing in gevent')
gevent.joinall(tasks)


print('\ntesting in multi-threading')
for url in urls:
    t = threading.Thread(target=get_body, args=(url,))
    t.start()
