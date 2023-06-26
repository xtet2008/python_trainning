# coding:utf-8
# @Time : 2023/2/8 21:31 
# @Author : Andy.Zhang
# @Desc :

import openai

response = openai.Image.create(
  prompt="a white siamese cat",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']