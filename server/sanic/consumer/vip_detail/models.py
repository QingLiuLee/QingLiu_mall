# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:10 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except


class VIPHistory(IEmbedded):
    pass


class ConsumerVIPDetail(IBaseModel):
    __slots__ = (
        'consumer_code',
        'create_time',
        'level',  # 等级
        'honorary_title',  # 荣誉称号
        'vip_history',
    )

    def __init__(self, **kwargs):
        super(ConsumerVIPDetail, self).__init__('consumer_vip_detail')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.level = kwargs.get('level', 0)
        self.honorary_title = kwargs.get('honorary_title', [])
        self.vip_history = kwargs.get('vip_history', [])
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    def init_vip_detail(cls, **kwargs):
        vip_detail = cls()
        vip_detail.consumer_code = kwargs.get('consumer_code', '')
        vip_detail.level = kwargs.get('level', 0)
        vip_detail.honorary_title = kwargs.get('honorary_title', [])
        vip_detail.vip_history = kwargs.get('vip_history', [])
        vip_detail.create_time = kwargs.get('create_time', None)
        return vip_detail

    @try_except
    def create_vip_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self


# class VIPPrivilege(IBaseModel):
#     """
#     VIP特权
#     """
#     __slots__ = {
#         'consumer_code',
#         'level',  # 等级
#         'honorary_title',  # 荣誉称号
#         'recharge_record',  # 充值记录
#     }
#
#     def __init__(self):
#         super(VIPPrivilege, self).__init__('consumer_vip_detail')
#         self.level = None
#         self.honorary_title = []
#         self.recharge_record = []
#
#     @try_except
#     def add_consumer_vip_honorary_title(self, honorary_title):
#         """添加消费者VIP荣耀称号"""
#         if all([self.consumer_code]):
#             return self.update_one_by_custom(
#                 condition={'consumer_code': self.consumer_code},
#                 update={'$push': {'vip_privilege.honorary_title': honorary_title}}
#             )
#         return None
#
#     @classmethod
#     @try_except
#     def init_vip_privilege(cls, **kwargs):
#         vip_privilege = cls()
#         vip_privilege.level = kwargs.get('level', None)
#         vip_privilege.honorary_title = kwargs.get('honorary_title', None)
#         vip_privilege.recharge_record = kwargs.get('recharge_record', None)
#         return vip_privilege
#
#     @try_except
#     def update_consumer_vip_privilege(self, vip_privilege):
#         """
#         更新消费者ＶＩＰ特权信息
#         :param vip_privilege:
#         :return:
#         """
#         if all([self.consumer_code, vip_privilege, vip_privilege.check_params_is_none()]):
#             return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
#                                              update={'$set': {'vip_privilege': vip_privilege.get_json_by_obj()}})
#         return None
#
#     @try_except
#     def update_consumer_vip_level(self, old_level, new_level):
#         """更新消费者VIP等级信息"""
#         if all([self.consumer_code]):
#             return self.update_one_by_custom(
#                 condition={'consumer_code': self.consumer_code, 'vip_privilege.level': old_level},
#                 update={'$set': {'vip_privilege.level': new_level}})
#         return None
