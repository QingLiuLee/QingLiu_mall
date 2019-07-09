# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IEmbedded, IBaseModel
from utils.decorator.exception import try_except


class IntegralHistoryInfo(IEmbedded):
    """
    integral list
    """
    __slots__ = {
        'income_type',  # 1:add  -1:reduce
        'integral_value',
        'create_time',
        'detail'
    }

    def __init__(self, **kwargs):
        super(IntegralHistoryInfo, self).__init__()
        self.income_type = kwargs.get('income_type', '')
        self.integral_value = kwargs.get('integral_value', 0)
        self.create_time = kwargs.get('create_time', None)
        self.detail = kwargs.get('detail', None)

    @classmethod
    def init_history_info(cls, **kwargs):
        history_info = cls()
        history_info.income_type = kwargs.get('income_type', 0)
        history_info.integral_value = kwargs.get('integral_value', 0)
        history_info.create_time = kwargs.get('create_time', datetime.datetime.now())
        history_info.detail = kwargs.get('detail', None)
        return history_info


class ConsumerIntegralDetail(IBaseModel):
    """
    积分
    """
    __slots__ = {
        'consumer_code',
        'total_integral',  # 总积分
        'create_time',
        'integral_history',  # 积分的历史列表 {'type':'收入', 'integral':'5', time:'2019/05/10', 'detail':{}}
    }

    def __init__(self, **kwargs):
        super(ConsumerIntegralDetail, self).__init__('consumer_integral_detail')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.total_integral = kwargs.get('total_integral', 0)
        self.integral_history = kwargs.get('integral_history', [])
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    @try_except
    def init_integral_detail(cls, **kwargs):
        integral = cls()
        integral.consumer_code = kwargs.get('consumer_code', '')
        integral.total_integral = kwargs.get('total_integral', 0)
        integral.integral_history = kwargs.get('integral_history', [])
        integral.create_time = kwargs.get('create_time', None)
        return integral

    @try_except
    def create_integral_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self.total_integral

    @try_except
    def update_consumer_integral_detail(self, integral_value, history_info: IntegralHistoryInfo):
        """
        更新消费者积分信息
        """
        return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                         update={
                                             '$inc': {'total_integral': integral_value},
                                             '$push': {'integral_history': history_info.get_json_by_obj()},
                                         })

    @try_except
    def get_integral_detail_by_consumer_code(self):
        return self.find_one(condition={'consumer_code': self.consumer_code})
