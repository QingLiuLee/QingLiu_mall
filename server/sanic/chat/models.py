# -*- coding: utf-8 -*-
# @Time     : 2019/7/10
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel, IEmbedded
from utils.decorator.exception import try_except


class ChatRecordInfo(IEmbedded):
    __slots__ = (
        'chat_record_code',
        'sender_code',
        'content',
        'send_time',
    )

    def __init__(self, **kwargs):
        super(ChatRecordInfo, self).__init__()
        self.chat_record_code = kwargs.get('chat_record_code', '')
        self.sender_code = kwargs.get('sender_code', '')
        self.content = kwargs.get('content', '')
        self.send_time = kwargs.get('send_time', None)

    @classmethod
    def init_chat_record(cls, **kwargs):
        chat_record = cls()
        chat_record.chat_record_code = kwargs.get('chat_record_code', '')
        chat_record.sender_code = kwargs.get('sender_code', '')
        chat_record.content = kwargs.get('content', '')
        chat_record.send_time = kwargs.get('send_time', None)
        return chat_record


class ChatRoom(IBaseModel):
    __slots__ = (
        'room_id',
        'is_org_room',
        'org_code',
        'org_staff_code_list',
        'consumer_code_list',
        'is_group',
        'create_time',
        'chat_record',
        'room_event',
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
        self.chat_record = kwargs.get('chat_record', [])
        self.room_event = kwargs.get('room_event', '')

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
        chat_room.chat_record = kwargs.get('chat_record', [])
        chat_room.room_event = kwargs.get('room_event', '')
        return chat_room

    @try_except
    def create_chat_room_info(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self

    @try_except
    def consumer_join_chat_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$push': {'consumer_code_list': consumer_code}}})

    @try_except
    def consumer_leave_chat_room(self, consumer_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$pull': {'consumer_code_list': consumer_code}}})

    @try_except
    def org_staff_join_chat_room(self, staff_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$push': {'org_staff_code_list': staff_code}}})

    @try_except
    def org_staff_leave_chat_room(self, staff_code):
        return self.update_one_by_custom(condition={'room_id': self.room_id},
                                         update={'$set': {'$pull': {'org_staff_code_list': staff_code}}})

    @try_except
    def get_chat_room_by_consumer_code(self, consumer_code):
        return self.find_many(condition={'consumer_code_list': consumer_code},
                              projection={'_id', 0})
