#!/usr/bin/env python
# encoding: utf-8
"""
@Author: ZhangSheng
@Contact: xtet2008@126.com
@File: 协程asyncio.py
@Time: 2018/9/30 0030 下午 20:01
@Software: PyCharm
@Desc: Python3.5协程学习研究  https://thief.one/2018/06/21/1/
"""


async def test1():
    print("1")
    print("2")


async def test2():
    print("3")
    print("4")


a = test1()  # RuntimeWarning: coroutine 'test1' was never awaited
b = test2()  # RuntimeWarning: coroutine 'test1' was never awaited

if False:
    # print(a, type(a))  # RuntimeWarning: coroutine 'test1' was never awaited
    # print(b, type(b))
    pass

if False:
    a.send(None)  # StopIteration
    b.send(None)

try:
    a.send(None)  # 可以通过 send方法，执行协程函数
except StopIteration as e:  # 协程函数执行结束时会抛出一个StopIteration异常，标志着协程函数执行结束，返回值在value中
    print(e.value)
    pass

try:
    b.send(None)
except StopIteration as e:
    print(e.value)
    pass


