#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 11:57
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : os_path.py

import os


source_dir_path = os.path.dirname (__file__)  # 返回文件路径
packed_path = os.path.join(source_dir_path, '..', os.path.basename(source_dir_path) + '_packed')
packed_path = os.path.normpath(packed_path)  # 规范path字符串形式

print packed_path