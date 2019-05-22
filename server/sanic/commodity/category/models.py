# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Category(IBaseModel):
    __slots__ = {
        'category_code',
        'org_code',
        'staff_code',
        'category_name',
        'create_time',
    }

    def __init__(self):
        super(Category, self).__init__('commodity_category')
        self.category_code = ''
        self.category_name = ''
        self.org_code = ''
        self.create_time = None

    @classmethod
    @try_except
    def init_category_info(cls, **kwargs):
        """
        初始化品类信息
        :param kwargs:
        :return:
        """
        category = cls()
        category.category_code = kwargs.get('category_code', '')
        category.org_code = kwargs.get('org_code', '')
        category.staff_code = kwargs.get('staff_code', '')
        category.category_name = kwargs.get('category_name', '')
        category.create_time = kwargs.get('create_time', None)
        return category

    @try_except
    def create_category_info(self):
        """
        创建新品类
        :return:
        """
        if all([self.category_name, self.org_code, self.staff_code]):
            self.category_code = make_code_or_id('C')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.category_code
        return False

    @try_except
    def update_category_info(self):
        """
        更新品类
        :return:
        """
        return self.update_one_by_custom(condition={'category_code': self.category_code},
                                         update={'$set': {'category_name': self.category_name}})

    @try_except
    def find_category_by_org_code_and_category_name(self):
        """
        根据商铺编码与品类名查找品类信息
        :return:
        """
        return self.find_one(condition={'org_code': self.org_code, 'category_name': self.category_name})

    @try_except
    def find_category_list_by_org_code(self):
        """获取商家品类信息"""
        return self.find(condition={'org_code': self.org_code}, projection={'_id': 0})
