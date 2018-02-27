#!/usr/bin/python
# -*- coding: UTF-8 -*-

thead = ['机构名称', '机构代码', '机构类型']
for col, item in enumerate(thead):
    pass
    # print col,item



fields = [
                {'name': '代理商'},
                {'username': '用户名'},
                {'agent_name': '姓名'},
                {'area_fullname': '负责区域'},
                {'school_count': '机构数'},
                {'classroom_count': '教室数'},
                {'init_classroom_num': '已安装教室数'}
            ]
for col, item in enumerate(fields):
    print col, item.values()[0]