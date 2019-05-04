# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe : 商家员工信息
import datetime
import hashlib

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
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

    @try_except
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
    @try_except
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

    @try_except
    def create_admin_info(self):
        """
        创建商家员工信息
        :return:
        """
        if all([self.mobile, self.nickname, self.password]):
            self.staff_code = make_code_or_id('S')
            self.password = hashlib.md5(self.password.encode("utf-8")).digest()
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.staff_code
        else:
            return None

    @try_except
    def find_staff_by_mobile_or_nickname(self, mobile='', nickname=''):
        return self.find_one(condition={'$or': [{'mobile': mobile}, {'nickname': nickname}]})

    @try_except
    def check_staff_password(self, password=''):
        """
        检测密码是否正确
        :return:
        """
        pwd_tmp = hashlib.md5(password.encode("utf-8")).digest()
        if self.password == pwd_tmp:
            return True
        return False

    @try_except
    def set_org_roles_by_staff_code(self, org_code='', role_code=''):
        """
        更新角色列表
        :return:
        """
        return self.update_one_by_custom(condition={'staff_code': self.staff_code}, update={
            '$push': {'roles': {'org_code': org_code, 'role_code': role_code}}})
