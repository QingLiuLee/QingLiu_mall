# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.util import make_code_or_id


class Category(IBaseModel):
    __slots__ = {
        'category_id',
        'category_name',
        'create_time',
    }

    def __init__(self, **kwargs):
        super(Category, self).__init__('category')

    def create_category_info(self, **kwargs):
        """
        ceate new category info
        :param kwargs:
        :return:
        """
        self.category_id = make_code_or_id('C')
        self.category_name = kwargs.get('category_name', '')
        self.create_time = datetime.datetime.now()
        self.create_info()
