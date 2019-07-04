# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
import datetime

import pymongo

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class LoginDetail(IBaseModel):
    __slots__ = {
        'code',
        'consumer_code',
        'create_time',
    }

    def __init__(self, **kwargs):
        super(LoginDetail, self).__init__('login_detail')
        self.code = kwargs.get('code', '')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    @try_except
    def init_detail_info(cls, **kwargs):
        login_detail = cls()
        login_detail.code = kwargs.get('code', '')
        login_detail.consumer_code = kwargs.get('consumer_code', '')
        login_detail.create_time = kwargs.get('create_time', None)
        return login_detail

    @try_except
    def create_login_detail_info(self):
        self.code = make_code_or_id('login_detail_')
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self.code

    @try_except
    def find_last_login_detail_by_consumer_code(self):
        return self.find_one(condition={'consumer_code': self.consumer_code}, sort_type=pymongo.DESCENDING)

    @try_except
    def get_login_detail_count_by_consumer_code(self):
        return self.get_info_count_by_filter(condition={'consumer_code': self.consumer_code})

    @try_except
    def check_login_detail_by_consumer_code_and_datetime(self, start_time, end_time):
        return self.find_one(condition={'$and': [{'consumer_code': self.consumer_code},
                                                 {'create_time': {"$gte": start_time, "$lt": end_time}}
                                                 ]})
