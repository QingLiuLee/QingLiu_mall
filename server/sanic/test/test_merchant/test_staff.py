# -*- coding: utf-8 -*-
# @Time     : 2019/5/12 下午1:45
# @Author   : Lee才晓
# @Describe :
import unittest

import requests

PROTOCOL = 'http://'
HOST = '127.0.0.1'
PORT = ':4001/'
VERSION = 'v1/'

BASE_URL = PROTOCOL + HOST + PORT + VERSION

CREATE_STAFF_INFO = BASE_URL + 'merchant/staff/create/administrators/info'
SIGN_IN = BASE_URL + 'merchant/staff/sign/in'


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

    def test_staff_create_info(self):
        data = {
            "mobile": "",
            "nickname": "",
            "password": ""
        }
        res = requests.post(CREATE_STAFF_INFO, data=data)
        print(res)

    def test_staff_sign_in(self):
        data = {
            "account": "13512722864",
            "password": "10241026"
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        res = requests.post(SIGN_IN, json=data, headers=headers, ).json()

        assert res.code == 200
        self.token = res.data.token
        self.staff_code = res.data.staff_code
