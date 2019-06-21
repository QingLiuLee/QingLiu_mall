#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 20:10
# @Author  : Lee才晓
# @File    : modes
# @Function:
import datetime

from bson import ObjectId

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Product(IBaseModel):
    __slots__ = {
        'product_code',
        'category_code',
        'org_code',
        'product_name',
        'img_list',
        'explain',
        'sale_price',
        'create_time',
        'currency',
    }

    def __init__(self):
        super(Product, self).__init__('commodity_product')
        self.product_code = ''
        self.category_code = ''
        self.product_name = ''
        self.org_code = ''
        self.img_list = []
        self.explain = ''
        self.sale_price = ''
        self.create_time = None
        self.currency = '¥'

    @classmethod
    @try_except
    def init_product_info(cls, **kwargs):
        product = cls()
        product.product_code = kwargs.get('product_code', '')
        product.category_code = kwargs.get('category_code', '')
        product.product_name = kwargs.get('product_name', '')
        product.org_code = kwargs.get('org_code', '')
        product.img_list = kwargs.get('img_list', [])
        product.explain = kwargs.get('explain', '')
        product.sale_price = kwargs.get('sale_price', '')
        product.create_time = kwargs.get('create_time', None)
        return product

    @try_except
    def create_product_info(self):
        """
        创建商品信息
        :return:
        """
        if all([self.category_code, self.product_name, self.org_code, self.sale_price]):
            self.product_code = make_code_or_id('P')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.product_code
        return False

    @try_except
    def find_info_by_org_code_and_product_name(self):
        """
        根据商铺编码与产品名称查找产品信息
        :return:
        """
        return self.find_one(condition={'org_code': self.org_code, 'product_name': self.product_name})

    @try_except
    def update_info_by_product_code(self):
        """
        根据产品编码更新产品信息
        :return:
        """
        return self.update_one_by_custom(condition={'product_code': self.product_code},
                                         update={'$set': {'product_name': self.product_name,
                                                          'img_list': self.img_list,
                                                          'explain': self.explain,
                                                          'sale_price': self.sale_price}})

    @try_except
    def delete_info_by_product_code(self, product_code_list):
        """根据产品ID删除产品"""
        return self.delete_many_by_condition(condition={'$and': [{'product_code': {'$in': product_code_list}},
                                                                 {'org_code': self.org_code}]})

    @try_except
    def find_product_list_by_org_code(self, category_type=[], last_id=None, limit=10, skip=0, turned=1):
        """获取商户下的产品列表"""

        condition = {'$and': [{'org_code': self.org_code}]}

        if category_type:
            condition['$and'].append({'category_code': {'$in': category_type}})

        if last_id:
            if turned > 0:
                _id = {'$gt': ObjectId(last_id)}
            else:
                _id = {'$lt': ObjectId(last_id)}
            condition['$and'].append({'_id': _id})

        return self.find_many(condition=condition, limit=limit, skip=skip)

    @try_except
    def get_all_product_count_by_org_code(self, category_type=[]):
        """获取产品的数量"""
        condition = {'$and': [{'org_code': self.org_code}]}

        if category_type:
            condition['$and'].append({'category_code': {'$in': category_type}})
        return self.get_info_count_by_filter(condition=condition)
