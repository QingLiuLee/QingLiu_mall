# -*- coding: utf-8 -*-
# @Time     : 5/6/19 7:02 PM
# @Author   : Lee才晓
# @Describe : 消费者模块
import datetime
import hashlib

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class ThirdPartyInfo(IEmbedded):
    """
    第三方信息
    """
    __slots__ = {
        'info_type',  # 第三方平台类型
        'uid',  # 第三方用户ID
        'open_id',  # 第三方开放ID
        'nickname',  # 第三方用户昵称
        'site_avatar',  # 第三方用户头像
        'access_token',  # 第三方token
        'create_time'  # 创建时间
    }

    pass


class ReceivingAddress(IEmbedded):
    """
    收货地址
    """
    __slots__ = {
        'address',  # 详细地址
        'region_code',  # 区域编码
        'mobile',  # 手机号
        'contacts',  # 联系人
    }

    def __init__(self):
        super(ReceivingAddress, self).__init__()
        self.address = ''
        self.region_code = ''
        self.mobile = ''
        self.contacts = ''

    @classmethod
    @try_except
    def init_receiving_address(cls, **kwargs):
        receive_address = cls()
        receive_address.address = kwargs.get('address', '')
        receive_address.region_code = kwargs.get('region_code', '')
        receive_address.mobile = kwargs.get('mobile', '')
        receive_address.contacts = kwargs.get('contacts', '')
        return receive_address


class ConsumerBaseInfo(IBaseModel):
    """
    基础信息
    """
    __slots__ = {
        'consumer_code',  # 编号
        'nickname',  # 昵称
        'password',  # 密码
        'mobile',  # 手机号
        'email',  # 邮箱
        'avatar',  # 头像
        'gender',  # 性别
        'birthday',  # 出生年月
        'intro',  # 简介
        'verify_id',  # 验证ID
        'receiving_address',  # 收货地址
        'third_party_info',  # 第三方信息
        'create_time',  # 创建时间
    }

    def __init__(self):
        super(ConsumerBaseInfo, self).__init__('consumer_base_info')
        self.consumer_code = ''
        self.nickname = ''
        self.password = ''
        self.mobile = ''
        self.email = ''
        self.avatar = ''
        self.gender = ''
        self.birthday = ''
        self.intro = ''
        self.verify_id = ''
        self.receiving_address = None
        self.third_party_info = None
        self.create_time = None

    @classmethod
    @try_except
    def init_base_info(cls, **kwargs):
        """
        初始化消费者基础信息
        :param kwargs:
        :return:
        """
        base_info = cls()
        base_info.consumer_code = kwargs.get('consumer_code', '')
        base_info.nickname = kwargs.get('nickname', '')
        base_info.password = kwargs.get('password', '')
        base_info.mobile = kwargs.get('mobile', '')
        base_info.email = kwargs.get('email', '')
        base_info.avatar = kwargs.get('avatar', '')
        base_info.gender = kwargs.get('gender', None)
        base_info.birthday = kwargs.get('birthday', None)
        base_info.intro = kwargs.get('intro', '')
        base_info.verify_id = kwargs.get('verify_id', '')
        base_info.receiving_address = kwargs.get('receiving_address', [])
        base_info.third_party_info = kwargs.get('third_party_info', None)
        base_info.create_time = kwargs.get('create_time', None)

        return base_info

    @try_except
    def find_consumer_by_mobile_or_nickname_or_email(self):
        """
        根据手机号或者昵称查找用户信息
        :return:
        """
        return self.find_one(condition={
            '$or': [{'mobile': self.mobile},
                    {'nickname': self.nickname},
                    {'email': self.email}]},
            projection={'_id': 0, 'create_time': 0, 'verify_id': 0, 'password': 0})

    @try_except
    def find_consumer_by_account(self, account):
        return self.find_one(condition={
            '$or': [{'mobile': account},
                    {'nickname': account},
                    {'email': account}]},
            projection={'_id': 0, 'create_time': 0, 'verify_id': 0, 'password': 0})

    @try_except
    def find_consumer_by_mobile_or_nickname_or_email_without_consumer_code(self):
        """过滤掉消费者编码获取消费者信息"""
        return self.find_one(condition={
            '$and': [{'consumer_code': {'$ne': self.consumer_code}},
                     {'$or': [{'mobile': self.mobile},
                              {'nickname': self.nickname},
                              {'email': self.email}]}]
        }, projection={'_id': 0, 'create_time': 0, 'verify_id': 0, 'password': 0})

    @try_except
    def find_consumer_by_consumer_code(self):
        """根据消费者编号获取消费者信息"""
        return self.find_one(condition={
            'consumer_code': self.consumer_code},
            projection={'_id': 0, 'create_time': 0, 'verify_id': 0, 'password': 0})

    @try_except
    def check_consumer_password(self, old_pwd='', new_pwd=''):
        """检测密码是否正确"""
        pwd_tmp = hashlib.md5(new_pwd.encode("utf-8")).digest()
        if old_pwd == pwd_tmp:
            return True
        return False

    @try_except
    def create_consumer_info(self):
        """
        创建消费者信息
        :return:
        """
        if all([self.mobile, self.nickname, self.password]):
            self.consumer_code = make_code_or_id('C')
            self.create_time = datetime.datetime.now()
            self.password = hashlib.md5(self.password.encode("utf-8")).digest()
            self.create_info()
            return self.consumer_code

        return None

    @try_except
    def update_consumer_base_info(self):
        """
        更新消费者信息
        :return:
        """
        if all([self.consumer_code, self.nickname, self.email]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code}, update={
                '$set': {'nickname': self.nickname, 'email': self.email, 'mobile': self.mobile,
                         'avatar': self.avatar, 'gender': self.gender, 'birthday': self.birthday,
                         'intro': self.intro}})
        return None

    @try_except
    def update_consumer_receiving_address(self, receiving_address: ReceivingAddress):
        """
        更新消费者收货地址信息
        :param receiving_address:
        :return:
        """
        if all([self.consumer_code, receiving_address, receiving_address.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': receiving_address.get_json_by_obj()}})
        return None

    @try_except
    def update_consumer_third_party_info(self, third_party_info: ThirdPartyInfo):
        """
        更新消费者第三方账号信息
        :param third_party_info:
        :return:
        """
        if all([self.consumer_code, third_party_info, third_party_info.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': third_party_info.get_json_by_obj()}})
        return None

    @try_except
    def add_consumer_receive_address(self, address: ReceivingAddress):
        """添加消费者收货地址"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code},
                update={'$push': {'receiving_address': address.get_json_by_obj()}}
            )
        return None

    @try_except
    def remove_consumer_receiver_address(self, address: ReceivingAddress):
        """移除消费者收货地址"""
        return self.update_one_by_custom(
            condition={'consumer_code': self.consumer_code},
            update={'$pull': {'receiving_address': {'address': address.address,
                                                    'region_code': address.region_code,
                                                    'mobile': address.mobile,
                                                    'contacts': address.contacts}}})

    @try_except
    def get_consumer_receiver_address(self):
        """获取消费者的收货地址"""

        return self.find_one(
            condition={'consumer_code': self.consumer_code},
            projection={'_id': 0, 'receiving_address': 1}
        )

    @try_except
    def get_consumer_pwd(self):
        """获取消费者的登录密码"""
        return self.find_one(
            condition={'consumer_code': self.consumer_code},
            projection={'_id': 0, 'password': 1, 'consumer_code': 1}
        )
