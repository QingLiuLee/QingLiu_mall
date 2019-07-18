# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
import datetime

import pymongo

from system.base_model import IBaseModel
from utils.constant import MESSAGE_TYPE
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class ChatRoom(IBaseModel):
    __slots__ = (
        'room_id',
        'is_org_room',
        'org_code',
        'org_staff_code_list',
        'consumer_code_list',
        'is_group',
        'create_time',
        'room_event',
        'admin_code',
        'room_name',
        'active_status',
    )

    def __init__(self, **kwargs):
        super(ChatRoom, self).__init__('chat_room')
        self.room_id = kwargs.get('room_id', '')
        self.is_org_room = kwargs.get('is_org_room', False)
        self.is_group = kwargs.get('is_group', False)
        self.org_staff_code_list = kwargs.get('org_staff_code_list', [])
        self.consumer_code_list = kwargs.get('consumer_code_list', [])
        self.create_time = kwargs.get('create_time', None)
        self.org_code = kwargs.get('org_code', '')
        self.room_event = kwargs.get('room_event', '')
        self.admin_code = kwargs.get('admin_code', '')
        self.room_name = kwargs.get('room_name', '')
        self.active_status = kwargs.get('active_status', False)

    @classmethod
    def init_chat_room(cls, **kwargs):
        chat_room = cls()
        chat_room.room_id = kwargs.get('room_id', '')
        chat_room.is_org_room = kwargs.get('is_org_room', False)
        chat_room.is_group = kwargs.get('is_group', False)
        chat_room.org_staff_code_list = kwargs.get('org_staff_code_list', [])
        chat_room.consumer_code_list = kwargs.get('consumer_code_list', [])
        chat_room.create_time = kwargs.get('create_time', None)
        chat_room.org_code = kwargs.get('org_code', '')
        chat_room.room_event = kwargs.get('room_event', '')
        chat_room.admin_code = kwargs.get('admin_code', '')
        chat_room.room_name = kwargs.get('room_name', '')
        chat_room.active_status = kwargs.get('active_status', False)
        return chat_room

    @try_except
    def create_chat_room_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self

    @try_except
    def consumer_join_chat_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$push': {'consumer_code_list': consumer_code}})

    @try_except
    def consumer_leave_chat_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$pull': {'consumer_code_list': consumer_code}})

    @try_except
    def org_staff_join_chat_room(self, staff_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$push': {'org_staff_code_list': staff_code}}})

    @try_except
    def org_staff_leave_chat_room(self, staff_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$pull': {'org_staff_code_list': staff_code}}})

    @try_except
    def get_chat_rooms_by_consumer_code(self, consumer_code):
        return self.find_many(condition={'$and': [{'consumer_code_list': consumer_code},
                                                  {'active_status': True}]},
                              projection={'_id': 0, 'create_time': 0},
                              sort_type=pymongo.DESCENDING)

    @try_except
    def get_rooms_id_by_consumer_code(self, consumer_code):
        return self.find_many(condition={'$and': [{'consumer_code_list': consumer_code},
                                                  {'active_status': True}]},
                              projection={'_id': 0, 'room_id': 1},
                              sort_type=pymongo.DESCENDING)

    @try_except
    def org_create_chat_room(self):
        self.room_id = make_code_or_id('chat_room_')
        self.create_time = datetime.datetime.now()
        self.room_event = MESSAGE_TYPE[0]
        self.is_org_room = True
        self.active_status = True
        self.create_info()
        return self

    @try_except
    def consumer_create_chat_room(self):
        self.room_id = make_code_or_id('chat_room_')
        self.room_event = MESSAGE_TYPE[0]
        self.create_time = datetime.datetime.now()
        self.is_org_room = False
        self.active_status = True
        self.create_info()
        return self

    @try_except
    def consumer_get_chat_room_by_code_and_id(self, consumer_code):
        return self.find_one(condition={'consumer_code_list': consumer_code,
                                        'room_id': self.room_id})

    @try_except
    def consumer_pull_to_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$pull': {'consumer_code_list': consumer_code}})

    @try_except
    def consuemr_push_to_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$push': {'consumer_code_list': consumer_code}})

    @try_except
    def org_update_chat_room_by_id(self):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'room_name': self.room_name,
                                                          'admin_code': self.admin_code}})

    @try_except
    def org_get_chat_room_by_id_and_admin_code(self):
        return self.find_one(condition={'$and': [{'room_id': self.room_id},
                                                 {'admin_code': self.admin_code}]})

    @try_except
    def org_push_staff_to_room(self, staff_code):
        return self.update_one_by_custom(condition={'$and': [{'room_id': self.room_id},
                                                             {'admin_code': self.admin_code}]},
                                         update={'$push': {'org_staff_code_list': staff_code}})

    @try_except
    def org_pull_staff_to_room(self, staff_code):
        return self.update_one_by_custom(condition={'$and': [{'room_id': self.room_id},
                                                             {'admin_code': self.admin_code}]},
                                         update={'$pull': {'org_staff_code_list': staff_code}})
