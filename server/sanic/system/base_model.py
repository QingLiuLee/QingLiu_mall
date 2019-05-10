# -*- coding: utf-8 -*-
# @Time     : 4/25/19 10:08 AM
# @Author   : Lee才晓
# @Describe :
from abc import ABCMeta

from bson import ObjectId

from system.database import MotorBase
from utils.decorator.exception import try_except


class IEmbedded(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def get_json_by_obj(self):
        """
        将类的属性转为字典
        :return:
        """
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value):
                pr[name] = value
        return pr

    @try_except
    def check_params_is_none(self, except_list=[]):
        """
        检测全部属性是否为空
        :param except_list: 特定属性除外
        :return:
        """
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value) and (value not in except_list) and (not value):
                return False
        return True


class IBaseModel(object):
    __metaclass__ = ABCMeta

    def __init__(self, collection):
        self.__db = MotorBase().get_db()
        self.__collection = self.__db[collection]

    def get_collection(self):
        return self.__collection

    def get_json_by_obj(self):
        """
        将类的属性转为字典
        :return:
        """
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value):
                pr[name] = value
        return pr

    def create_info(self, model_info=None):
        if not model_info:
            model_info = self.get_json_by_obj()

        return self.__collection.insert_one(model_info)

    def get_info_by_last_id_and_page_size(self, last_id, page_size=10):

        return self.__collection.find({'_id': {'$gt': ObjectId(last_id)}}).limit(page_size)

    def delete_info_by_id(self, model_id=None):

        return self.__collection.find_one_and_delete({'_id': model_id})

    def update_info_by_id(self, model_id=None, model_info=None):
        if model_id and model_info:
            return self.__collection.find_one_and_update(filter={'_id': model_id}, update=model_info)
        return False

    def find_one_and_update_info_by_custom(self, condition=None, info_json=None):
        """
        根据自定义条件更新一条数据
        :return:
        """
        if condition and info_json:
            return self.__collection.find_one_and_update(filter=condition, update=info_json)
        return False

    def update_one_by_custom(self, condition=None, update=None):
        """
        根据自定义条件更新数据
        :return:
        """
        if condition and update:
            return self.__collection.update_one(filter=condition, update=update)
        return False

    def update_many(self, condition=None, update_info=None):
        if filter and update_info:
            return self.__collection.update_many(filter=condition, update=update_info)

    def find_one(self, condition={}, stipulated={}):
        return self.__collection.find_one(filter=condition, **stipulated)
