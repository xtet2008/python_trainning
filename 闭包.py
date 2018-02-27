#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/24 11:36
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : 闭包.py


def make_adder(addend):
    def adder(augend):
        return augend + addend
    return adder


p = make_adder(23)
q = make_adder(44)

print p(100)
print q(100)