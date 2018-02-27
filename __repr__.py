#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 定义函数


class Test_Class(object):

    def __str__(self):  # to_string()
        return "__str__"

    def __repr__(self):
        return "__repr__"

obj = Test_Class()

print '%s' % obj  # __str__
print '%r' % obj  # __repr__

