# -*- coding: utf-8 -*-
# @Time     : 2019/5/12 下午1:42
# @Author   : Lee才晓
# @Describe :
import unittest

import requests

PROTOCOL = 'http://'
HOST = '127.0.0.1'
PORT = ':8000/'
VERSION = 'v1/'

BASE_URL = PROTOCOL + HOST + PORT + VERSION
SIGN_IN = BASE_URL + 'merchant/staff/sign/in'
create_merchant_info = BASE_URL + 'merchant/organization/create/info'
get_org_list = BASE_URL + 'merchant/organization/get/info/list'


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

    def test_create_merchant_info(self):
        data = {
            'staff_code': self.staff_code,
            'org_name': '商铺名称',
            'explain': '简介',
            'img_list': ['图片地址'],
            'sale_type': ['美妆', '家电']
        }
        headers = {
            'Authorization-token': self.token
        }
        res = requests.post(create_merchant_info, json=data, headers=headers).json()
        print('test_create_merchant_info')
        print(res)

    def test_get_org_list(self):
        data = {
            'staff_code': self.staff_code,
        }
        headers = {
            'Authorization-token': self.token
        }
        res = requests.post(get_org_list, json=data, headers=headers).json()
        print('test_get_org_list')
        print(res)
