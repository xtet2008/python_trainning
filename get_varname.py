#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 18:57
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : get_varname.py


import inspect, re

# https://www.zhihu.com/question/42768955

def varname(p):
    funcname= 'varname'
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\b%s\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)' %funcname, line)
    if m:
        return m.group(1)


if __name__ == '__main__':
    shit = 233
    print varname(shit)