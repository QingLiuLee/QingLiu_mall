# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except


class OrderHistory(IEmbedded):
    __slots__ = (
        'order_code',
        'create_time',
    )

    def __init__(self, **kwargs):
        super(OrderHistory, self).__init__()
        self.order_code = kwargs.get('order_code', '')
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    def init_order_history(cls, **kwargs):
        order_history = cls()
        order_history.order_code = kwargs.get('order_code', '')
        order_history.create_time = kwargs.get('create_time', None)
        return order_history


class ConsumerOrderDetail(IBaseModel):
    __slots__ = {
        'consumer_code',
        'create_time',
        'order_history',
    }

    def __init__(self, **kwargs):
        super(ConsumerOrderDetail, self).__init__('consumer_order_detail')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.create_time = kwargs.get('create_time', None)
        self.order_history = kwargs.get('order_history', [])

    @classmethod
    def init_order_detail(cls, **kwargs):
        order_detail = cls()
        order_detail.consumer_code = kwargs.get('consumer_code', '')
        order_detail.create_time = kwargs.get('create_time', None)
        order_detail.order_history = kwargs.get('order_history', [])
        return order_detail

    @try_except
    def create_order_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self
