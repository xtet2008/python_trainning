# -*- coding: utf-8 -*-

from M2Crypto import BIO, RSA, EVP
import base64
import datetime
import json
import urllib
import requests

import logging
# _logger = logging.getLogger(__name__)


class ali_pay(object):
    def request_f2f_barcode_pay(self):

        ali_app_id = '2016010501065642'
        sign_type = 'RSA'
        alipay_rsa_key = '''
        -----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCxbLD/b/cPKn5xk3IEPMDeo/FSL5Vr6DvvA52aTTZQMJYN/9yI
zPwr+bZ+FDIn9LSXpdu4Nzt09GWD7Hrk9q188Gmhp8IDOl0m7ggMeYogWEfaxqEx
0SBLEfgWHIC9YF0agES5TwGD3h6jbP1gm3maQkVYCZ+wLUafXhys3+8qawIDAQAB
AoGBAJPtLFF8l38UjeHB7jDsOl4mUACW3bzfHoE0AYXx1FPdfm5jogqI5cMAaxAJ
ZJv9oUhCp8OagT8MuUrZsskNhiyeL61nJ6ZS0ji6OTH/tkxmmR6MYzDvzTVG64Tv
25wH0Dr6s9mYy5MtbSHlYUZ7VSh2JfzLbnIN4x9EdJ4dejDJAkEA3/TgVbAdy7zZ
YTcOpwcfNS1r6O/RdOEiHDYejhQ4XGBvvmqzo+gz4E7cbo1E2FOKA0BueRWNh8fY
j3KBceGxrQJBAMrPbtqQ7mIZrFn84EOn+Wg62BY9J9f8I460YEpjfLiOIvC+8gVF
z9ptmCPmPpuACZ/pAg1C3046rqcao1v8P3cCQQCskyEPRpAfQB3uSKPU16sXqjGe
JLatrxI+1QFEkJZBsNpKzCQzaKoY7gv0cI2dePo/uTWnvpD6EWhyWVUgMT9dAkBU
fRHrT9FfYN6iJmyvAr0uJMV8jkGZAts1SgOLOeLtZ5k6vfFJLQooLtvgqLyQP0jD
K2jFaYRprJyx1LEVUwKFAkEAvCIAwms2vW7Wytvf0+uXliP0xYeb5WxAVpoziv7N
0PYPenaM4lppNzjgbl9o8TjYsbMu5towFYNXzpXBmySoEg==
-----END RSA PRIVATE KEY-----
'''
        alipay_rsa_key = alipay_rsa_key.strip()
        notify_url = None
        biz_content = self.get_biz_content()
        _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        req_param = {
            # 'alipay_sdk':'alipay-sdk-java-dynamicVersionNo',
            'app_id': ali_app_id,  # '2016010501065642',
            'biz_content': json.dumps(biz_content).encode('utf-8'),
            'charset': 'utf-8',
            'format': 'json',
            # 'method': 'alipay.trade.pay',
            'method': 'alipay.trade.refund',
            'sign_type': sign_type,
            # 'timestamp': '2016-01-06 00:00:00',
            'timestamp': _now,
            'version': '1.0',
        }
        if notify_url:
            req_param.update({'notify_url': notify_url})
        md = ''
        if sign_type == 'RSA':
            md = 'sha1'
        elif sign_type == 'RSA2':
            md = 'sha256'
        if md:
            sign = self._generate_sign_rsa(req_param, alipay_rsa_key, md=md)
        else:
            sign = self._generate_sign_rsa(req_param, alipay_rsa_key)
        # sign = self._generate_sign_rsa(cr, uid, req_param, alipay_rsa_key)
        req_param['biz_content'] = urllib.quote(req_param['biz_content'], safe='{}:"~()*!.\'')  # for py2
        req_param['sign'] = urllib.quote(sign, safe='~()*!.\'')  # for py2
        req_param = '&'.join(['%s=%s' % (key, value) for key, value in sorted(req_param.items())])

        print(u'\n request parameters：', req_param)
        date = datetime.datetime.now()
        result = self.send_post_request("openapi.alipay.com", "/gateway.do", req_param)
        print ("\n api time cost: ", (datetime.datetime.now() - date).seconds)

        result = json.loads(result, 'GBK')
        print("\nResult of /gateway.do: %s" % str(result))

        if result and result['alipay_trade_refund_response']:
            req_content = result['alipay_trade_refund_response']
            if req_content['code'] == '10000':
                print(u'处理完成')
                # 支付成功暂时注释掉
                # wf_service = netsvc.LocalService("workflow")
                # wf_service.trg_validate(uid, 'nt.payment.alipay', ali_pay_id, 'pay_paid', cr)
            else:
                print('%s,%s' % (req_content['sub_code'], req_content['sub_msg'],))

    def _generate_sign_rsa(self, params, alipay_rsa_key, md='sha1'):
        message = '&'.join(['%s=%s' % (key, value) for key, value in sorted(params.items())])
        print('需签名字符串为：')
        print(message)

        key = EVP.load_key_string(str(alipay_rsa_key))  # for py2
        # key = EVP.load_key_string(alipay_rsa_key.encode('utf-8'))  # for py3
        key.reset_context(md=md)
        key.sign_init()
        key.sign_update(message.encode('utf-8'))
        signature = key.sign_final()
        result = base64.b64encode(signature)
        print('签名结果字符串为：')
        print(result)
        return result

    def get_biz_content(self,
                        out_biz_no="2008B24E0004",
                        alipay_trade_no="2021112422001412345705862663",
                        alipay_uid="2088502178512340",
                        order_pay_time="2021-11-24 15:13:12"
                        ):
        biz_content = {
            "out_trade_no": '20212008C10E0001_144927',  # nt_payment_alipay.name
            "refund_amount": 0.01,
            "out_request_no": 'BSTESTALIPAY210039532',
            # "trade_no":'2021112422001434285702932376',
        }

        print('\n biz_content:')
        print(biz_content)
        print('\n')

        return biz_content


    def send_post_request(self, domain, url, post_body, timeout=30):


        headers = {"content-type": "application/x-www-form-urlencoded","charset": "utf-8"}
        # conn = httplib.HTTPSConnection(domain, timeout=timeout)
        # conn.request("POST", url, post_body, headers)


        # str_result = conn.getresponse(buffering=True).read()
        req_url = 'https://%s%s'%(domain, url)
        # requests.packages.urllib3.disable_warnings()
        response = requests.post(url=req_url, data=post_body, headers=headers, verify=False, timeout=timeout)
        str_result = response.text
        print(response.json())
        return str_result

    
if __name__ == '__main__':
    Ali = ali_pay()
    # Ali.get_biz_content()
    Ali.request_f2f_barcode_pay()