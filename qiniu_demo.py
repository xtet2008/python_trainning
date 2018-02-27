#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 18:26
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : qiniu_demo.py

from qiniu import Auth, put_file
import os
import zlib


def get_file_crc(file_path):
    result = None

    if os.path.isfile(file_path):
        result = format(zlib.crc32(open(file_path).read()) & 0xFFFFFFFFL, '08x')

    return result


def upload_file_to_qiniu(file_path):
    file_url = None

    if not file_path or not os.path.isfile(file_path):
        raise Exception('no specify the file or file not exist: %s' % file_path)

    file_name = get_file_crc(file_path)
    file_extension = os.path.splitext(file_path)[1]

    bucket_name = 'theone-doremi'
    my_qiniu_domain = 'p174ci935.bkt.clouddn.com'
    access_key = 'RqRHNMDNh4EklCQwTqUDWJrTnLPnHidoRBGjTFH0'
    secret_key = 'xZ104y1OTOgmcBOppRtwabiY32xeuNkLC5HOJrUf'

    q = Auth(access_key=access_key, secret_key=secret_key)
    key = file_name + file_extension
    policy = {'insertOnly': 0}

    token = q.upload_token(bucket_name, key, 3600, policy=policy)
    ret, info = put_file(token, key, file_path)
    if info.status_code == 200 and info.exception is None:
        file_url = 'http://%s/%s' % (my_qiniu_domain, ret['key'])

    return file_url



print upload_file_to_qiniu(file_path='/Users/xiaoyezi/work/doremi/doremi/../data/files/license_agreement/3.pdf')
