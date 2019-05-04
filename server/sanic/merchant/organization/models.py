# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:13 PM
# @Author   : Lee才晓
# @Describe : 商家信息表
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Organization(IBaseModel):
    """
    商家信息
    """
    __slots__ = {
        'merchant_code',  # 商家编码
        'merchant_name',  # 商家名
        'explain',  # 商家简介
        'create_time',  # 创建时间
        'img_list',  # 商家图片展示
        'owner_code',  # 商家负责人用户编码
        'sale_type',  # 售货类型
    }

    def __init__(self):
        super(Organization, self).__init__('merchant')
        self.merchant_code = ''
        self.merchant_name = ''
        self.explain = ''
        self.create_time = None
        self.img_list = []
        self.owner_code = ''
        self.sale_type = []

    @classmethod
    def init_org_info(cls, **kwargs):
        """
        初始化商家信息
        :param kwargs:
        :return:
        """
        org = cls()
        org.merchant_code = kwargs.get('merchant_code', '')
        org.merchant_name = kwargs.get('merchant_name', '')
        org.explain = kwargs.get('explain', '')
        org.create_time = kwargs.get('create_time', None)
        org.img_list = kwargs.get('img_list', [])
        org.owner_code = kwargs.get('owner_code', '')
        org.sale_type = kwargs.get('sale_type', [])

        return org

    @try_except
    def create_org_info(self):
        """
        创建商家信息
        :return:
        """

        if all([self.merchant_name, self.img_list, self.sale_type]):
            self.merchant_code = make_code_or_id('M')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.merchant_code
        else:
            return None

    def set_org_owner(self, owner_code):
        """
        设置商家负责人编码
        :param owner_code:
        :return:
        """
        if owner_code:
            self.owner_code = owner_code
            self.find_one_and_update_info_by_custom(condition={'merchant_code': self.merchant_code},
                                                    info_json=self.get_json_by_obj())

    @try_except
    def find_org_by_merchant_name(self, merchant_name=''):
        """
        根据商铺名称查找
        :param merchant_name:
        :return:
        """
        return self.find_one(condition={'merchant_name': merchant_name})
