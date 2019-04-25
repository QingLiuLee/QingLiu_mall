# -*- coding: utf-8 -*-
# @Time     : 4/25/19 10:08 AM
# @Author   : Lee才晓
# @Describe :
from abc import ABCMeta

from system.database import MotorBase


class IBaseModel(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.motor = MotorBase()
        self.db = self.motor.get_db()

    def get_info_list_by_pageSize(self):
        result = self.db.users.find_one({})
        return result
