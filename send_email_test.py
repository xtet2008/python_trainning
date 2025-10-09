#!/usr/bin/python
# Write Python 3 code in this online editor and run it.
print("Hello, World!");


def send_email_to_andy_on_failure(context):
    import requests
    import json

    # print("send email to andy")
    html_content = f"<html>\n<head></head>\n<body>\n<h1>{context}</h1>\n<p>Best Regards.</p>\n</body>\n</html>"
    payload = {
        "subject": "Debug-Airflow",
        "recipient_list": ["xtet2008@126.com"],
        "body_html": html_content
    }
    token = 'abc'

    url = "https://api-test.silicondata.com/api/system/send-email"
    method = "POST"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    # response = requests.request(method, url, headers=headers, data=payload, timeout=10)
    response = requests.request(method, url, headers=headers, data=json.dumps(payload))
    status_code = response.status_code
    response_json = response.json()
    print(status_code)
    print(response_json)


send_email_to_andy_on_failure(context='abcd')
