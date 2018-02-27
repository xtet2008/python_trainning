#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/28 14:32
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : tesseract.py

import pytesseract
from PIL import Image

image = Image.open('/Users/xiaoyezi/test2.png')
image.load()
image.show()
vcode = pytesseract.image_to_string(image)
print vcode