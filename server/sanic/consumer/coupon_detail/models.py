# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:13 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except


class CouponHistory(IEmbedded):
    __slots__ = {
        'coupon_code',
        'create_time',  # get it time
        'is_used',
        'vail_status',  # 1、无效 2、有效
    }

    def __init__(self, **kwargs):
        super(CouponHistory, self).__init__()
        self.coupon_code = kwargs.get('coupon_code', '')
        self.create_time = kwargs.get('create_time', None)
        self.is_used = kwargs.get('is_used', 0)
        self.vail_status = kwargs.get('vail_status', 0)

    @classmethod
    def init_coupon_history(cls, **kwargs):
        coupon_history = cls()
        coupon_history.coupon_code = kwargs.get('coupon_code', '')
        coupon_history.create_time = kwargs.get('create_time', None)
        coupon_history.is_used = kwargs.get('is_used', 0)
        coupon_history.vail_status = kwargs.get('vail_status', 0)
        return coupon_history


class ConsumerCouponDetail(IBaseModel):
    """
    优惠券
    """

    __slots__ = {
        'consumer_code',
        'create_time',
        'coupon_history',
    }

    def __init__(self, **kwargs):
        super(ConsumerCouponDetail, self).__init__('consumer_coupon_detail')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.create_time = kwargs.get('consumer_code', None)
        self.coupon_history = kwargs.get('coupon_history', [])

    @classmethod
    def init_coupon_detail(cls, **kwargs):
        coupon_detail = cls()
        coupon_detail.consumer_code = kwargs.get('consumer_code', '')
        coupon_detail.create_time = kwargs.get('consumer_code', None)
        coupon_detail.coupon_history = kwargs.get('coupon_history', [])
        return coupon_detail

    @try_except
    def create_coupon_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self

    @try_except
    def update_consumer_coupon(self, coupon):
        """
        更新消费者优惠券信息
        :param coupon:
        :return:
        """
        if all([self.consumer_code, coupon, coupon.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': coupon.get_json_by_obj()}})
        return None
