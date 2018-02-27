#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/22 17:14

from time import ctime,sleep
import threading

def music(func):
    for i in range(2):
        print "I was listening to %s. %s" % (func,ctime())
        sleep(1)

def move(func):
    for i in range(2):
        print "I was at the %s. %s" % (func,ctime())
        sleep(5)


threads = []
t1 = threading.Thread(target=music, args=('爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move, args=('阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()  # 合并线程，join()前面的线程代码运行完后，才执行 join() 后面的代码。
    # join()让一个线程B“加入”到另外一个线程A的尾部。在A执行完毕之前，B不能工作. 也可在括号里面加入 nSeconds 超时限制，如果超过这个时间，则停止等待，后面的代码变为可运行状态。
    print "all over %s" % ctime()
