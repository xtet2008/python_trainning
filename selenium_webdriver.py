# coding:utf-8
# @Time : 2023/7/25 01:13 
# @Author : Andy.Zhang
# @Desc :



import time
from time import sleep
from splinter import Browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# type = sys.stdout.encoding



def login_and_get_token(username, password):
    # Replace 'webdriver' with the appropriate webdriver, e.g., 'chrome', 'firefox', etc.
    # with Browser('chrome') as browser:
    with Browser('webdriver') as browser:
        # Navigate to the login page
        browser.visit('https://bdoos.com')
        sleep(10)

        browser.driver.find_elements(By.TAG_NAME, "a")[6].click()  # 登录
        sleep(3)

        # Find and fill in the login form
        # You may need to inspect the login form to find the proper input field names or IDs.
        browser.find_by_name('email').fill(username)
        browser.find_by_name('passwd').fill(password)

        # Submit the login form
        browser.driver.find_element(By.ID, "login_submit").click()

        # Wait for some time to ensure the login process completes
        time.sleep(5)

        # Get the token after successful login
        # token = get_token(browser)  # Define get_token() function (see next step)
        # return token

        get_cookies(browser)


def get_cookies(browser):
    cookies = browser.driver.get_cookies()
    for cookie in cookies:
        print(cookie)

def get_token(browser):
    # Replace 'TOKEN_ELEMENT_SELECTOR' with the appropriate selector to locate the token element.
    # This could be a CSS selector, XPATH, or any other method supported by Splinter/Selenium.
    # You may need to inspect the page source to find the selector for the token element.
    token_element = browser.find_by_css('TOKEN_ELEMENT_SELECTOR').first

    if token_element:
        token = token_element.text
        return token

    # If the token element is not found, handle the error appropriately.
    raise ValueError("Token element not found.")







if __name__ == "__main__":
    # Replace 'YOUR_USERNAME' and 'YOUR_PASSWORD' with your actual login credentials.
    username = 'xtet2008@126.com'
    password = 'zhang+sheng=zqf'

    print('\n\nbegain show cookies \n\n')


    # token = login_and_get_token(username, password)
    if False:
        login_and_get_token(username, password)

    # Store the token in a file or database, etc., for later use.
    # with open('token.txt', 'w') as f:
    #     f.write(token)

    print("\n\n Cookie has been successfully retrieved and stored.")






    share_links = [
        'vmess://eyJob3N0IjoiIiwicGF0aCI6IiIsInRscyI6IiIsInZlcmlmeV9jZXJ0Ijp0cnVlLCJhZGQiOiJ6ajkubW1vZHMuc2l0ZSIsInBvcnQiOjMzNDMzLCJhaWQiOjAsIm5ldCI6InRjcCIsImhlYWRlclR5cGUiOiJub25lIiwidiI6IjIiLCJ0eXBlIjoidm1lc3MiLCJwcyI6IkFB5paw5Yqg5Z2hNyB2MnJheSBwbGF55ZWG5bqX5LiL6L2955SoIOe9keWdgDpiZG9vcy5jb20iLCJyZW1hcmsiOiJBQeaWsOWKoOWdoTcgdjJyYXkgcGxheeWVhuW6l + S4i + i9veeUqCDnvZHlnYA6YmRvb3MuY29tIiwiaWQiOiJjM2I3MDllOC0yY2UxLTM0NDYtYWU4My1mNTlhNGEyNTRlYjgiLCJjbGFzcyI6Mn0 =',
        'vmess://eyJ2IjoiMiIsInBzIjoiQUHmlrDliqDlnaE3IHYycmF5IHBsYXnllYblupfkuIvovb3nlKgg572R5Z2AOmJkb29zLmNvbSIsImFkZCI6InpqOS5tbW9kcy5zaXRlIiwicG9ydCI6IjMzNDMzIiwiaWQiOiJjM2I3MDllOC0yY2UxLTM0NDYtYWU4My1mNTlhNGEyNTRlYjgiLCJhaWQiOiIwIiwibmV0IjoidGNwIiwidHlwZSI6Im5vbmUiLCJob3N0IjoiIiwicGF0aCI6IiIsInRscyI6IiJ9'
    ]

    import base64
    import json


    def parse_vmess_url(vmess_url):
        # Remove the "vmess://" prefix and decode the Base64-encoded URL
        decoded_vmess = base64.urlsafe_b64decode(vmess_url[8:]).decode('utf-8')

        # Load the JSON data
        vmess_data = json.loads(decoded_vmess)

        return vmess_data


    # Python保存为json中文Unicode乱码解决 json.dump()
    # 参考链接：https://blog.csdn.net/baidu_36499789/article/details/121371587

    # Example V2Ray "vmess" URL
    # vmess_url = "vmess://eyJ2IjoiMiIsInBzIjoi5L2g5aW9Iiwic2N5Ijoi5L2g5aW9IiwidHlwZSI6Im5vbmUiLCJob3N0IjoiaHR0cHM6Ly9leGFtcGxlLmNvbSIsInBhdGgiOiIvd2ViIiwidiI6IjIifQ=="
    for vmess_url in share_links:
        parsed_vmess_data = parse_vmess_url(vmess_url)
        json_str = json.dumps(parsed_vmess_data, indent=4, ensure_ascii=False)
        print(json_str)
