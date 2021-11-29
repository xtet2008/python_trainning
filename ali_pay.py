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

        ali_app_id = ''  # SLT支付宝配置，郑浩测试和张胜测试也只有减塑1个，马志宇能收着两个（减塑和电子小票）
        # ali_app_id = ''  # Only支付宝配置，用陈艺文测试，只有减塑，没有电子小票，
        # ali_app_id = ''  # JJ支付宝支付，马晓松测试，也只有减塑，没有电子小票
        # ali_app_id = ''  # VM支付宝配置，国义能收着两个球

        sign_type = 'RSA'
        alipay_rsa_key = '''
        -----
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
            'method': 'alipay.commerce.receipt.send',
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

        if result and result['alipay_commerce_receipt_send_response']:
            req_content = result['alipay_commerce_receipt_send_response']
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
                        out_biz_no="2008B29E0001",
                        alipay_trade_no="",
                        alipay_uid="",
                        order_pay_time="2021-11-24 15:13:12"
                        ):
        order_info = {
            "out_biz_no": out_biz_no,
            "pay_type": "alipay",  # 支付类型：支付宝
            "alipay_uid": alipay_uid,  # "2088002492134283",  # 支付宝用户uid，2088902576524349
            "order_type": "FASHION",  # 品牌
            "pay_amount": 99.00,  # 实际支付的金额，两位小数
            "trade_type": "TRADE",  # 交易号类型，默认 TRADE
            "trade_no": alipay_trade_no,  # 订单所对应的支付宝交易号
            "order_pay_time": order_pay_time,  # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 订单支付时间
            "merchant_name": "ONLY",  # 商户名字，建议写 绫致，或 brand_name
            "shop_name": "杭州_工联大厦_ONLY",  # 门店名称; 拥有门店的场景时，必填; 否则无法展示门店信息
            "environmental_info": [
                {
                    "environmental": "A",  # 环保类型: A:减塑/不使用购 物袋; B:无纸质小票
                    "environmental_ext": "huanbaojiansu",  # 环保行为内容字典值: 减塑/不使用购物袋:huanbaojiansu;
                },
                {
                    "environmental": "B",  # 环保类型: A:减塑/不使用购 物袋; B:无纸质小票
                    "environmental_ext": "dianzixiaopiao",  # 环保行为内容字典值: 无纸质小票(电子小票):dianzixiaopiao;
                }
            ]
        }

        biz_content = {
            "order_list": [
                order_info
            ]
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