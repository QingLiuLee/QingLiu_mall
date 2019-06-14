# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:13 PM
# @Author   : Lee才晓
# @Describe :
from system.base_model import IEmbedded
from utils.decorator.exception import try_except


class Coupon(IEmbedded):
    """
    优惠券
    """

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