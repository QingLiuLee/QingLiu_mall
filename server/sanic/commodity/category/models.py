# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel


class Category(IBaseModel):

    __slots__ = {
        'category_id',
        'category_name',
        'create_time',
    }

    def __init__(self):
        super(Category, self).__init__('category')

    def init_data(self, **kwargs):
        self.category_id =
        self.category_name = kwargs.get('category_name', '')
        self.create_time = datetime.datetime.now()



