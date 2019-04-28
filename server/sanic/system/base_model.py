# -*- coding: utf-8 -*-
# @Time     : 4/25/19 10:08 AM
# @Author   : Lee才晓
# @Describe :
from abc import ABCMeta

from bson import ObjectId

from system.database import MotorBase


class IBaseModel(object):
    __metaclass__ = ABCMeta

    def __init__(self, collection):
        self.__db = MotorBase().get_db()
        self.__collection = self.__db[collection]

    def get_json_by_obj(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value):
                pr[name] = value
        return pr

    def get_obj_by_dic(self, json={}):
        top = type('new', (object,), json)
        seqs = tuple, list, set, frozenset
        for i, j in json.items():
            if isinstance(j, dict):
                setattr(top, i, self.get_obj_by_dic(j))
            elif isinstance(j, seqs):
                setattr(top, i,
                        type(j)(self.get_obj_by_dic(sj) if isinstance(sj, dict) else sj for sj in j))
            else:
                setattr(top, i, j)
        return top

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

    def update_many(self, condition=None, update_info=None):
        if filter and update_info:
            return self.__collection.update_many(filter=condition, update=update_info)
