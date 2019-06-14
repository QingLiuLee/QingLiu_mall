# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
from system.base_model import IEmbedded
from utils.decorator.exception import try_except


class Integral(IEmbedded):
    """
    积分
    """
    __slots__ = {
        'total_integral',  # 总积分
        'history_list',  # 积分的历史列表 {'type':'收入', 'integral':'5', time:'2019/05/10'}
    }

    def __init__(self):
        super(Integral, self).__init__()
        self.total_integral = 0
        self.history_list = []

    @classmethod
    @try_except
    def init_integral(cls, **kwargs):
        integral = cls()
        integral.total_integral = kwargs.get('total_integral', 0)
        integral.history_list = kwargs.get('history_list', [])
        return integral

    @try_except
    def update_consumer_integral(self, integral):
        """
        更新消费者积分信息
        :param integral:
        :return:
        """
        if all([self.consumer_code, integral, integral.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': integral.get_json_by_obj()}})
        return None