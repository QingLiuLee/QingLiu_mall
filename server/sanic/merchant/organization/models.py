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
        'org_code',  # 商家编码
        'org_name',  # 商家名
        'explain',  # 商家简介
        'create_time',  # 创建时间
        'img_list',  # 商家图片展示
        'staff_code',  # 商家负责人用户编码
        'sale_type',  # 售货类型
    }

    def __init__(self):
        super(Organization, self).__init__('merchant_org')
        self.org_code = ''
        self.org_name = ''
        self.explain = ''
        self.create_time = None
        self.img_list = []
        self.staff_code = ''
        self.sale_type = []

    @classmethod
    def init_org_info(cls, **kwargs):
        """
        初始化商家信息
        :param kwargs:
        :return:
        """
        org = cls()
        org.org_code = kwargs.get('org_code', '')
        org.org_name = kwargs.get('org_name', '')
        org.explain = kwargs.get('explain', '')
        org.create_time = kwargs.get('create_time', None)
        org.img_list = kwargs.get('img_list', [])
        org.staff_code = kwargs.get('staff_code', '')
        org.sale_type = kwargs.get('sale_type', [])

        return org

    @try_except
    def create_org_info(self):
        """
        创建商家信息
        :return:
        """

        if all([self.org_name, self.img_list, self.sale_type]):
            self.org_code = make_code_or_id('M')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.org_code
        else:
            return None

    @try_except
    def find_org_by_org_name(self):
        """
        根据商铺名称查找
        """
        return self.find_one(condition={'org_name': self.org_name})

    @try_except
    def update_merchant_info(self):
        """
        更新商铺信息
        :return:
        """
        return self.update_one_by_custom(condition={'org_code': self.org_code}, update={'$set': {
            'org_name': self.org_name,
            'explain': self.explain,
            'img_list': self.img_list,
            'sale_type': self.sale_type
        }})

    @try_except
    def find_all_org_list_by_staff_code(self):
        """根据管理员编码获取商家列表"""
        return self.find(condition={'staff_code': self.staff_code},
                         projection={'_id': 0, })
