# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe : 商家员工信息
import datetime
import hashlib

from bson import ObjectId

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Roles(IEmbedded):
    """角色信息"""

    __slots__ = {
        'role_name',
        'org_code',
        'start_time',
        'end_time',
    }

    @try_except
    def __init__(self):
        super(Roles, self).__init__()
        self.role_name = ''
        self.org_code = ''
        self.start_time = None
        self.end_time = None

    @classmethod
    @try_except
    def ini_roles_data(cls, **kwargs):
        role = Roles()
        role.role_name = kwargs.get('role_name', '')
        role.org_code = kwargs.get('org_code', '')
        role.start_time = kwargs.get('start_time', None)
        role.end_time = kwargs.get('end_time', None)

        return role


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
    def set_org_roles_by_staff_code(self, staff_code='', org_code='', role_name=''):
        """
        添加角色信息
        :return:
        """

        role = Roles.ini_roles_data(org_code=org_code, role_name=role_name, start_time=datetime.datetime.now())

        return self.update_one_by_custom(condition={'staff_code': staff_code}, update={
            '$push': {'roles': role.get_json_by_obj()}})

    @try_except
    def get_staff_info_by_staff_code(self):
        """根据员工编码获取员工信息"""
        return self.find_one(condition={'staff_code': self.staff_code})

    @try_except
    def get_staff_list_by_org_code(self, org_code, role_type=[], last_id=None, limit=10, skip=0, turned=1):
        """ 根据商家编码获取员工列表"""

        condition = {'$and': [{'roles.org_code': org_code}]}

        if role_type:
            condition['$and'].append({'roles.role_name': {'$in': role_type}})

        if last_id:
            if turned > 0:
                condition['$and'].append({'_id': {'$gt': ObjectId(last_id)}})
            else:
                condition['$and'].append({'_id': {'$lt': ObjectId(last_id)}})

        return self.find_many(condition=condition, projection={'password': 0}, limit=limit, skip=skip)

    @try_except
    def get_all_staff_count_by_org_code(self, org_code, role_type=[]):
        """根据商家编码获取员工数量"""

        condition = {'$and': [{'roles.org_code': org_code}]}
        if role_type:
            condition['$and'].append({'roles.role_name': {'$in': role_type}})

        return self.get_info_count_by_filter(condition=condition)

    @try_except
    def remove_account(self):
        """删除账号信息"""
        condition = {'staff_code': self.staff_code}
        return self.delete_one_by_condition(condition=condition)

    @try_except
    def get_role_info_by_org_code(self, role_list, org_code):
        """根据商户编码获取当前用户的角色信息"""
        if not role_list or not org_code:
            return False

        for role in role_list:
            if role['org_code'] == org_code and not role['end_time']:
                return role

        return False

    @try_except
    def set_role_end_time_by_org_code(self, org_code):
        """根据商户编码设置角色的结束时间(移除该角色)"""
        return self.update_one_by_custom(condition={'$and': [{'staff_code': self.staff_code},
                                                             {'roles.org_code': org_code}]}, update={
            '$set': {'roles.$.end_time': datetime.datetime.now()}})
