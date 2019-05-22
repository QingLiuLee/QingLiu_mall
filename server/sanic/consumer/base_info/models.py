# -*- coding: utf-8 -*-
# @Time     : 5/6/19 7:02 PM
# @Author   : Lee才晓
# @Describe : 消费者模块
import datetime
import hashlib

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class ConsumerBaseInfo(IEmbedded):
    """
    基础信息
    """
    __slots__ = {
        'nickname',  # 昵称
        'password',  # 密码
        'mobile',  # 手机号
        'email',  # 邮箱
        'avatar',  # 头像
        'gender',  # 性别
        'birthday',  # 出生年月
        'intro',  # 简介
    }

    def __init__(self):
        super(ConsumerBaseInfo, self).__init__()
        self.nickname = ''
        self.password = ''
        self.mobile = ''
        self.email = ''
        self.avatar = ''
        self.gender = ''
        self.birthday = ''
        self.intro = ''

    @classmethod
    @try_except
    def init_base_info(cls, **kwargs):
        """
        初始化消费者基础信息
        :param kwargs:
        :return:
        """
        base_info = cls()
        base_info.nickname = kwargs.get('nickname', '')
        base_info.password = kwargs.get('password', '')
        base_info.mobile = kwargs.get('mobile', '')
        base_info.email = kwargs.get('email', '')
        base_info.avatar = kwargs.get('avatar', '')
        base_info.gender = kwargs.get('gender', None)
        base_info.birthday = kwargs.get('birthday', None)
        base_info.intro = kwargs.get('intro', '')

        return base_info


class VIPPrivilege(IEmbedded):
    """
    VIP特权
    """
    __slots__ = {
        'level',  # 等级
        'honorary_title',  # 荣誉称号
        'recharge_record',  # 充值记录
    }

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


class Coupon(IEmbedded):
    """
    优惠券
    """
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


class Consumer(IBaseModel):
    """
    消费者信息
    """
    __slots__ = {
        'consumer_code',
        'base_info',
        'vip_privilege',
        'create_time',
        'integral',
        'coupon',
        'receiving_address',
        'third_party_info'
    }

    @try_except
    def __init__(self):
        super(Consumer, self).__init__('consumer')
        self.consumer_code = ''
        self.base_info = None
        self.create_time = None
        self.vip_privilege = None
        self.integral = None
        self.coupon = None
        self.receiving_address = None
        self.third_party_info = None

    @classmethod
    @try_except
    def init_consumer_info(cls, **kwargs):
        """
        初始化消费者信息
        :param kwargs:
        :return:
        """
        consumer = cls()
        consumer.consumer_code = kwargs.get('consumer_code', '')
        consumer.base_info = kwargs.get('base_info', None)
        consumer.create_time = kwargs.get('create_time', None)
        consumer.vip_privilege = kwargs.get('vip_privilege', None)
        consumer.integral = kwargs.get('integral', None)
        consumer.coupon = kwargs.get('coupon', None)
        consumer.receiving_address = kwargs.get('receiving_address', None)
        consumer.third_party_info = kwargs.get('third_party_info', None)

        return consumer

    @try_except
    def find_consumer_by_mobile_or_nickname(self):
        """
        根据手机号或者昵称查找用户信息
        :return:
        """
        return self.find_one(condition={
            '$or': [{'base_info.mobile': self.base_info['mobile']},
                    {'base_info.nickname': self.base_info['nickname']}]},
            stipulated={'_id': 0, 'base_info': 1, 'base_info.password': 0, 'create_time': 1,
                        'vip_privilege': 1, 'integral': 1, 'coupon': 1, 'receiving_address': 1,
                        'third_party_info': 1})

    @try_except
    def check_consumer_password(self, password=''):
        """检测密码是否正确"""
        pwd_tmp = hashlib.md5(password.encode("utf-8")).digest()
        if self.base_info['password'] == pwd_tmp:
            return True
        return False

    @try_except
    def create_consumer_info(self):
        """
        创建消费者信息
        :return:
        """
        if all([self.base_info]):
            self.consumer_code = make_code_or_id('C')
            self.create_time = datetime.datetime.now()
            self.base_info['password'] = hashlib.md5(self.base_info['password'].encode("utf-8")).digest()
            self.create_info()
            return self.consumer_code
        return None

    @try_except
    def update_consumer_base_info(self, base_info: ConsumerBaseInfo):
        """
        更新消费者信息
        :return:
        """
        if all([self.consumer_code, base_info, base_info.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code}, update={
                '$set': {'base_info': base_info.get_json_by_obj()}})
        return None

    @try_except
    def update_consumer_vip_privilege(self, vip_privilege: VIPPrivilege):
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
    def update_consumer_integral(self, integral: Integral):
        """
        更新消费者积分信息
        :param integral:
        :return:
        """
        if all([self.consumer_code, integral, integral.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': integral.get_json_by_obj()}})
        return None

    @try_except
    def update_consumer_coupon(self, coupon: Coupon):
        """
        更新消费者优惠券信息
        :param coupon:
        :return:
        """
        if all([self.consumer_code, coupon, coupon.check_params_is_none()]):
            return self.update_one_by_custom(condition={'consumer_code': self.consumer_code},
                                             update={'$set': {'integral': coupon.get_json_by_obj()}})
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
    def update_consumer_vip_level(self, old_level, new_level):
        """更新消费者VIP等级信息"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code, 'vip_privilege.level': old_level},
                update={'$set': {'vip_privilege.level': new_level}})
        return None

    @try_except
    def add_consumer_vip_honorary_title(self, honorary_title):
        """添加消费者VIP荣耀称号"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code},
                update={'$push': {'vip_privilege.honorary_title': honorary_title}}
            )
        return None

    @try_except
    def add_consumer_receive_address(self, address: ReceivingAddress):
        """添加消费者收货地址"""
        if all([self.consumer_code]):
            return self.update_one_by_custom(
                condition={'consumer_code': self.consumer_code},
                update={'$push': {'receiving_address': address}}
            )
        return None
