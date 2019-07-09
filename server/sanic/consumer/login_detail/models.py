# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
import datetime
from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class LoginHistory(IEmbedded):
    __slots__ = {
        'login_history_code',
        'create_time',
    }

    def __init__(self, **kwargs):
        super(LoginHistory, self).__init__()
        self.login_history_code = kwargs.get('login_history_code', make_code_or_id('login_history_code_'))
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    def init_login_history(cls, **kwargs):
        login_history = cls()
        login_history.login_history_code = kwargs.get('login_history_code', make_code_or_id('login_history_code_'))
        login_history.create_time = kwargs.get('create_time', datetime.datetime.now())
        return login_history


class ConsumerLoginDetail(IBaseModel):
    __slots__ = {
        'consumer_code',
        'create_time',
        'login_history'
    }

    def __init__(self, **kwargs):
        super(ConsumerLoginDetail, self).__init__('consumer_login_detail')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.create_time = kwargs.get('create_time', None)
        self.login_history = kwargs.get('login_history', [])

    @classmethod
    @try_except
    def init_login_detail(cls, **kwargs):
        login_detail = cls()
        login_detail.consumer_code = kwargs.get('consumer_code', '')
        login_detail.create_time = kwargs.get('create_time', None)
        login_detail.login_history = kwargs.get('login_history', [])
        return login_detail

    @try_except
    def create_login_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self

    @try_except
    def add_login_history(self, login_history: LoginHistory):
        return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                         update={'$push': {'login_history': login_history.get_json_by_obj()}})

    @try_except
    def find_login_detail_by_consumer_code(self):
        return self.find_one(condition={'consumer_code': self.consumer_code})

    @try_except
    def get_login_history_by_consumer_code(self):
        return self.find_one(condition={'consumer_code': self.consumer_code})

    @try_except
    def get_login_detail_count_by_consumer_code(self):
        return self.get_info_count_by_filter(condition={'consumer_code': self.consumer_code})

    @try_except
    def check_login_detail_by_consumer_code_and_datetime(self, start_time, end_time):
        return self.find_one(condition={'$and': [{'consumer_code': self.consumer_code},
                                                 {'login_history.create_time': {"$gte": start_time, "$lt": end_time}}
                                                 ]})
