# -*- coding: utf-8 -*-
# @Time     : 4/25/19 10:08 AM
# @Author   : Lee才晓
# @Describe :
from abc import ABCMeta
from system.database import MotorBase
from utils.decorator.exception import try_except


class IEmbedded(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @try_except
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

    @try_except
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
            if not name.startswith('__') and not callable(value) and (name not in except_list) and (not value):
                return False
        return True

    @try_except
    def create_info(self, model_info=None):
        if not model_info:
            model_info = self.get_json_by_obj()

        return self.__collection.insert_one(model_info)

    @try_except
    def update_one_by_custom(self, condition=None, update=None):
        """根据自定义条件更新一条数据"""
        if condition and update:
            return self.__collection.update_one(filter=condition, update=update)
        return False

    @try_except
    def update_many_by_condition(self, condition=None, update=None):
        """根据自定义条件更新多条数据"""
        if condition and update:
            return self.__collection.update_many(filter=condition, update=update)
        return False

    @try_except
    def find_one(self, condition={}, stipulated={}):
        return self.__collection.find_one(filter=condition, **stipulated)

    @try_except
    def find_many(self, condition={}, projection={}, limit=10):
        if not projection:
            return self.__collection.find(filter=condition).to_list(length=limit)
        return self.__collection.find(filter=condition, projection=projection).to_list(length=limit)

    @try_except
    def get_info_count_by_filter(self, condition):
        """根据条件获取总数量"""
        return self.__collection.count_documents(filter=condition)

    @try_except
    def delete_many_by_condition(self, condition):
        return self.__collection.delete_many(filter=condition)

    @try_except
    def delete_one_by_condition(self, condition):
        return self.__collection.delete_one(filter=condition)

    @try_except
    def drop_collection(self):
        """清空collection"""
        return self.__collection.drop()
