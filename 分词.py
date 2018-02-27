#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/19 16:13
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : 分词.py

import jieba

print ' '.join(jieba.cut('这是我的写作，我想搜索一些关键词'))