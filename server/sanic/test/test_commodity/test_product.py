# -*- coding: utf-8 -*-
# @Time     : 2019/5/12 下午3:30
# @Author   : Lee才晓
# @Describe :
import sys
import unittest

import requests

PROTOCOL = 'http://'
HOST = '127.0.0.1'
PORT = ':8000/'
VERSION = 'v1/'

BASE_URL = PROTOCOL + HOST + PORT + VERSION
SIGN_IN = BASE_URL + 'merchant/staff/sign/in'

create_product_info = BASE_URL + 'commodity/product/create/info'


class Test(unittest.TestCase):

    def setUp(self) -> None:
        data = {
            "account": "13512722864",
            "password": "10241026"
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        res = requests.post(SIGN_IN, json=data, headers=headers, ).json()

        assert res['code'] == 200
        self.token = res['data']['token']
        self.staff_code = res['data']['staff_code']

    def test_create_category_info(self):
        data = {
            'category_code': '美妆',
            'product_name': self.staff_code,
            'org_code': 'M2019051214370353',
            'img_list': ['产品图片'],
            'explain': '产品简介',
            'sale_price': '100'
        }
        headers = {
            'Authorization-token': self.token
        }
        res = requests.post(create_product_info, json=data, headers=headers).json()
        print(sys._getframe().f_code.co_name)
        print(res)
