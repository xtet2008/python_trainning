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
import urllib.request as urllib
monkey.patch_all()


def get_body(i):
    print ('start', i)
    urllib.urlopen("http://www.baidu.com")
    print ('end', i)


tasks = [gevent.spawn(get_body, i) for i in range(3)]
# print (tasks)
print ('testing in gevent')
gevent.joinall(tasks)

print ('\ntesting in threading')
for i in range(3):
    t = threading.Thread(target=get_body, args=(i,))
    t.start()
