# -*- coding: utf-8 -*-
# @Time     : 6/17/19 7:23 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Coupon(IBaseModel):
    __slots__ = {
        'coupon_code',  # 优惠券编码
        'title',  # 标题/名称
        'create_time',  # 创建时间
        'start_time',  # 有效开始时间
        'end_time',  # 有效结束时间
        'explain',  # 说明
        'total_num',  # 总量
        'used_num',  # 已使用量
        'received_num',  # 已发行量
        'distribution_form_type',  # 发行形式　１、现金　２、折扣
        'distribution_form_value',  # 优惠值
        'use_threshold',  # 使用门槛 1、不限制　２、满ＸＸＸ可使用
        'available_product_type',  # 可用商品 1、全场　２、指定商品
        'available_product_list',  # 可用商品列表
        'limit_num',  # 每人限制数量
        'consumer_type',  # 消费者类型　1、不限　２、普通用户　３、VIP用户
        'consumer_value',  # 消费者列表
        'vail_status',  # 1、无效 2、有效  由审核模块管理
    }

    def __init__(self, **kwargs):
        super(Coupon, self).__init__('coupon')
        self.coupon_code = kwargs.get('coupon_code', '')
        self.title = kwargs.get('title', '')
        self.create_time = kwargs.get('create_time', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.explain = kwargs.get('explain', '')
        self.total_num = kwargs.get('total_num', 0)
        self.used_num = kwargs.get('used_num', 0)
        self.received_num = kwargs.get('received_num', 0)
        self.distribution_form_type = kwargs.get('distribution_form_type', 1)
        self.distribution_form_value = kwargs.get('distribution_form_value', 0)
        self.use_threshold = kwargs.get('use_threshold', 1)
        self.available_product_type = kwargs.get('available_product_type', 1)
        self.available_product_list = kwargs.get('available_product_list', [])
        self.limit_num = kwargs.get('limit_num', 0)
        self.consumer_type = kwargs.get('consumer_type', 1)
        self.consumer_value = kwargs.get('consumer_value', [])

    @classmethod
    @try_except
    def init_coupon_info(cls, **kwargs):
        coupon = cls()
        coupon.coupon_code = kwargs.get('coupon_code', '')
        coupon.title = kwargs.get('title', '')
        coupon.create_time = kwargs.get('create_time', None)
        coupon.start_time = kwargs.get('start_time', None)
        coupon.end_time = kwargs.get('end_time', None)
        coupon.explain = kwargs.get('explain', '')
        coupon.total_num = kwargs.get('total_num', 0)
        coupon.used_num = kwargs.get('used_num', 0)
        coupon.received_num = kwargs.get('received_num', 0)
        coupon.distribution_form_type = kwargs.get('distribution_form_type', 1)
        coupon.distribution_form_value = kwargs.get('distribution_form_value', 0)
        coupon.use_threshold = kwargs.get('use_threshold', 1)
        coupon.available_product_type = kwargs.get('available_product_type', 1)
        coupon.available_product_list = kwargs.get('available_product_list', [])
        coupon.limit_num = kwargs.get('limit_num', 0)
        coupon.consumer_type = kwargs.get('consumer_type', 1)
        coupon.consumer_value = kwargs.get('consumer_value', [])
        return coupon

    @try_except
    def create_coupon_info(self):
        """创建优惠券信息"""
        self.coupon_code = make_code_or_id('C')
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self.coupon_code

    @try_except
    def find_coupon_by_title(self):
        return self.find_one(condition={'title': self.title})

    @try_except
    def find_coupon_by_coupon_code(self):
        return self.find_one(condition={'coupon_code': self.coupon_code})
