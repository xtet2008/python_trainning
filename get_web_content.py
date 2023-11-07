# coding:utf-8
# @Time : 2023/7/27 02:17 
# @Author : Andy.Zhang
# @Desc :

import requests
from bs4 import BeautifulSoup





# 设置 POST 请求的 URL 和数据
login_url = 'https://www.0dianyun11.xyz/auth/login'  # 替换为实际的登录 URL
data = {'email': 'xtet2008@126.com', 'passwd': 'zhang+sheng=zqf'}  # 替换为实际的用户名和密码

# 发送 POST 请求
response = requests.post(login_url, data=data)

# 检查响应状态码是否为 200，表示请求成功
if response.status_code == 200:
    # 读取返回的 cookies 值
    cookies = response.cookies

    # 使用 cookies 值进行后续操作
    # 例如，发送带有 cookies 的 GET 请求
    node_url = 'https://www.0dianyun11.xyz/user/node'  # 替换为需要使用 cookies 的 URL
    another_response = requests.get(node_url, cookies=cookies)

    # 打印获取到的数据
    print(another_response.text)




    soup = BeautifulSoup(another_response.content, 'html.parser')

    # Find all paragraphs
    paragraphs = soup.find_all('p')

    # Extract and print the text from each paragraph
    for paragraph in paragraphs:
        print(paragraph.get_text())


    node_vpn_url_ssr_jp1 = 'https://www.0dianyun11.xyz/user/nodeinfo/87'
    node_vpn_url_v2ray_sinpor7 = 'https://www.0dianyun11.xyz/user/nodeinfo/110'
    node_vpn = requests.get(node_vpn_url_v2ray_sinpor7, cookies=cookies)
    print(node_vpn.json())


else:
    print("POST request failed with status code:", response.status_code)
