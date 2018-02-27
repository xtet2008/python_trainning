#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/30 14:30
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : err_cacth.py


def dim(x, y):
    return x/y if not x and not y else None

class ZeroErr(Exception):
    pass


def main():
    try:
        print (3/0)
    except Exception, msg:
        raise ZeroErr(msg)

main()