# -*- coding: utf-8 -*-
# @Time     : 2019/7/3
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Integral(IBaseModel):
    __slots__ = {
        'integral_code',
        'integral_value',
        'explain',
        'create_time',
    }

    def __init__(self, **kwargs):
        super(Integral, self).__init__('integral')
        self.integral_code = kwargs.get('integral_code', '')
        self.integral_value = kwargs.get('integral_value', 0)
        self.explain = kwargs.get('explain', '')
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    @try_except
    def init_integral_info(cls, **kwargs):
        integral = cls()
        integral.integral_code = kwargs.get('integral_code', '')
        integral.integral_value = kwargs.get('integral_value', 0)
        integral.explain = kwargs.get('explain', '')
        integral.create_time = kwargs.get('create_time', None)
        return integral

    @try_except
    def create_integral_info(self):
        self.integral_code = make_code_or_id('I')
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self.integral_code

    @try_except
    def update_integral_info(self):
        return self.update_one_by_custom(condition={'integral_code': self.integral_code},
                                         update={'$set': {'integral_value': self.integral_value,
                                                          'explain': self.explain}})

    @try_except
    def find_integral_by_code(self):
        return self.find_one(condition={'integral_code': self.integral_code})

    @try_except
    def find_integral_by_value(self):
        return self.find_one(condition={'integral_value': self.integral_value})

    @try_except
    def delete_integral_info(self):
        return self.delete_one_by_condition(condition={'integral_code': self.integral_code})
