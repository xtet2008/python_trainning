# coding:utf-8
# @Time : 2024/6/9 下午2:27 
# @Author : Andy.Zhang
# @Desc :
import json

import aiohttp
import asyncio
import pandas as pd
import urllib.parse
from aiohttp import ClientSession

'''
base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112306852189221875844_1717914484267&sortColumns=PF_START_DATE,NOTICE_DATE,SECURITY_CODE,HOLDER_NAME,PF_NUM&sortTypes=-1,-1,-1,-1,-1&pageSize=50&pageNumber=1&reportName=RPTA_APP_ACCUMDETAILS&columns=ALL&quoteColumns=&source=WEB&client=WEB"

base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get
    callback=jQuery112306852189221875844_1717914484267
    &sortColumns=PF_START_DATE,NOTICE_DATE,SECURITY_CODE,HOLDER_NAME,PF_NUM&sortTypes=-1,-1,-1,-1,-1&pageSize=50&pageNumber=1&reportName=RPTA_APP_ACCUMDETAILS&columns=ALL&quoteColumns=&source=WEB&client=WEB"
'''

jquery_key = "jQuery112306852189221875844_1717914484267"
base_url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?'  # 替换为实际的URL
payload = {
    "callback": jquery_key,
    "sortColumns": "PF_START_DATE%2CNOTICE_DATE%2CSECURITY_CODE%2CHOLDER_NAME%2CPF_NUM",
    "sortTypes": "-1%2C-1%2C-1%2C-1%2C-1",
    "pageSize": "500",
    "pageNumber": "1",
    "reportName": "RPTA_APP_ACCUMDETAILS",
    "columns": "ALL",
    "quoteColumns": "",
    "source": "WEB",
    "client": "WEB",
}

headers_mapping = {
    "SECURITY_CODE": "股票代码",
    "SECURITY_NAME_ABBR": "股票简称",
    "HOLDER_NAME": "股东名称",
    "PF_NUM": "质押股份数量(股)",  # 1000.00 万  10000000,
    "PF_HOLD_RATIO": "占所持股份比例(%)",
    "PF_TSR": "占总股本比例(%)",
    "PF_ORG": "质押机构",
    "CLOSE_PRICE": "最新价(元)",
    "CLOSE_FORWARD_ADJPRICE_TODAY": "质押日收盘价(元)",
    "OPENLINE": "预估平仓线(元)",
    "PF_START_DATE": "质押开始日期",
    "NOTICE_DATE": "公告日期",
    "STOCK_DETAIL": "相关详情",  # "https://data.eastmoney.com/gpzy/detail/603270.html"
    "STOCK_DATA": "相关数据",  # "https://data.eastmoney.com/stockdata/603270.html",
    "PAGE_NUMBER": "页数",
}


public_stock_data = []


def format_stock_data(source_stock_data: dict, page_number):
    if not source_stock_data:
        return False

    SECURITY_CODE = source_stock_data.get("SECURITY_CODE")
    if not SECURITY_CODE:
        return False

    stock_data = {}
    keys = headers_mapping.keys()
    for head in keys:
        value = source_stock_data.get(head)
        value = '-' if value is None else value
        #stock_data[head] = value
        stock_data[headers_mapping[head]] = value
    else:
        # stock_data["STOCK_DETAIL"] = f"https://data.eastmoney.com/gpzy/detail/{SECURITY_CODE}.html"
        # stock_data["STOCK_DATA"] = f"https://data.eastmoney.com/stockdata/{SECURITY_CODE}.html"
        stock_data[headers_mapping["STOCK_DETAIL"]] = f"https://data.eastmoney.com/gpzy/detail/{SECURITY_CODE}.html"
        stock_data[headers_mapping["STOCK_DATA"]] = f"https://data.eastmoney.com/stockdata/{SECURITY_CODE}.html"
        # stock_data[headers_mapping["PAGE_NUMBER"]] = f"{page_number}"
        stock_data[headers_mapping["PAGE_NUMBER"]] = int(page_number)


    public_stock_data.append(stock_data)

    return True


def build_csv_data(data_list: list, page_number: int):
    if not data_list:
        return False

    for data in data_list:
        format_stock_data(data, page_number)

    return True


async def fetch(session, url):
    headers = {'Content-Type': 'application/json'}
    async with session.get(url, headers=headers) as response:
        result_text = await response.text()
        result = ""
        if jquery_key in result_text:
            # download success
            result_text = result_text.replace(f"{jquery_key}(", "")
            result_text = result_text.replace("});", "}")
            result = result_text

            page_number = 1
            try:
                position = url.find("pageNumber")
                if position != -1:
                    end_position = position + 20
                    substring = url[position:end_position]
                    page_number = substring.split("&")[0].split("=")[1]

                result = json.loads(result)
                if result.get("success") and result.get("success") and result.get("code") == 0:
                    result = result["result"]["data"]
                    build_csv_data(result, page_number)
                else:
                    result = {}
            except Exception as e:
                result = {}
                print(str(e))

        return result


async def fetch_all(urls):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


def save_to_csv(data, filename='results.csv'):
    # df = pd.DataFrame(data, columns=[head for head in headers_mapping.keys()])
    df = pd.DataFrame(data, columns=[headers_mapping[head] for head in headers_mapping.keys()])
    df.to_csv(filename, index=False)


async def main():
    urls = []
    for i in range(1, 55):
        query_string, key_maps = "", []
        for key, value in payload.items():
            if key == "pageNumber":
                value = f"{i}"
            key_maps.append('='.join([key, value]))
        else:
            query_string = '&'.join(key_maps)
        # query_string = urllib.parse.urlencode(payload)
        urls.append(f'{base_url}{query_string}')

    results = await fetch_all(urls)

    sorted_data = sorted(public_stock_data, key=lambda x: (x[headers_mapping.get("PAGE_NUMBER")]))
    # 按 PAGE_NUMBER 升序, PF_START_DATE 降序
    # sorted_data = sorted(public_stock_data,
    #                      key=lambda x: (x[headers_mapping.get("PAGE_NUMBER")], -x[headers_mapping.get("PF_START_DATE")]))
    save_to_csv(sorted_data)


if __name__ == '__main__':
    asyncio.run(main())
