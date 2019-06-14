# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:10 PM
# @Author   : Lee才晓
# @Describe :
from system.base_model import IEmbedded
from utils.decorator.exception import try_except


class VIPPrivilege(IEmbedded):
    """
    VIP特权
    """
    __slots__ = {
        'level',  # 等级
        'honorary_title',  # 荣誉称号
        'recharge_record',  # 充值记录
    }

    @try_except
    def add_consumer_vip_honorary_title(self, honorary_title):
        """添加消费者VIP荣耀称号"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code},
                update={'$push': {'vip_privilege.honorary_title': honorary_title}}
            )
        return None
    def __init__(self):
        super(VIPPrivilege, self).__init__()
        self.level = None
        self.honorary_title = []
        self.recharge_record = []

    @classmethod
    @try_except
    def init_vip_privilege(cls, **kwargs):
        vip_privilege = cls()
        vip_privilege.level = kwargs.get('level', None)
        vip_privilege.honorary_title = kwargs.get('honorary_title', None)
        vip_privilege.recharge_record = kwargs.get('recharge_record', None)
        return vip_privilege

    @try_except
    def update_consumer_vip_privilege(self, vip_privilege):
        """
        更新消费者ＶＩＰ特权信息
        :param vip_privilege:
        :return:
        """
        if all([self.consumer_code, vip_privilege, vip_privilege.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'vip_privilege': vip_privilege.get_json_by_obj()}})
        return None

    @try_except
    def update_consumer_vip_level(self, old_level, new_level):
        """更新消费者VIP等级信息"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code, 'vip_privilege.level': old_level},
                update={'$set': {'vip_privilege.level': new_level}})
        return None


