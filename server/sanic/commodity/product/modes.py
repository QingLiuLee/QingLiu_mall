#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 20:10
# @Author  : Lee才晓
# @File    : modes
# @Function:
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Product(IBaseModel):
    __slots__ = {
        'product_code',
        'category_code',
        'merchant_code',
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
        self.merchant_code = ''
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
        product.merchant_code = kwargs.get('merchant_code', '')
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
        if all([self.category_code, self.product_name, self.merchant_code, self.sale_price]):
            self.product_code = make_code_or_id('P')
            self.create_time = datetime.datetime.now()
            self.create_info()
            return self.product_code
        return False

    @try_except
    def find_info_by_merchant_code_and_product_name(self):
        """
        根据商铺编码与产品名称查找产品信息
        :return:
        """
        return self.find_one(condition={'merchant_code': self.merchant_code, 'product_name': self.product_name})

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
