# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe : 商家员工信息
import datetime

from system.base_model import IBaseModel
from utils.util import make_code_or_id


class Staff(IBaseModel):
    """
    商家员工信息
    """
    __slots__ = {
        'staff_code',  # 员工编码
        'mobile',  # 手机号
        'nickname',  # 昵称
        'password',  # 密码
        'create_time',  # 创建时间
        'avatar',  # 头像地址
        'roles',  # 相对应商家的角色
    }

    def __init__(self):
        super(Staff, self).__init__('merchant_staff')
        self.staff_code = ''
        self.mobile = ''
        self.nickname = ''
        self.password = ''
        self.create_time = None
        self.avatar = ''
        self.roles = []

    @classmethod
    def init_staff_info(cls, **kwargs):
        """
        初始化员工信息
        :param kwargs:
        :return:
        """
        staff = cls()
        staff.staff_code = kwargs.get('staff_code', '')
        staff.mobile = kwargs.get('mobile', '')
        staff.nickname = kwargs.get('nickname', '')
        staff.password = kwargs.get('password', '')
        staff.create_time = kwargs.get('create_time', None)
        staff.avatar = kwargs.get('avatar', '')
        staff.roles = kwargs.get('roles', [])
        return staff

    def create_staff_info(self):
        """
        创建商家员工信息
        :return:
        """
        if all([self.mobile, self.nickname, self.password]):
            self.staff_code = make_code_or_id('S')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.staff_code
        else:
            return None
