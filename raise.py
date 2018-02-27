#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 定义函数


def mye(level):
    if level < 1:
        raise Exception("Invalid level!", level)
        # 触发异常后，后面的代码就不会再执行
try:
    print 'begain'
    mye(0)  # 触发异常
    'end'
except "Invalid level!":
    print 1
else:
    print 2
