# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
import datetime

import pymongo
from bson import ObjectId

from system.base_model import IBaseModel
from utils.decorator.exception import try_except


class ChatRecord(IBaseModel):
    __slots__ = (
        'room_id',
        'create_time',
        'sender_code',
        'message_content',
        'message_type',

    )

    def __init__(self, **kwargs):
        super(ChatRecord, self).__init__('chat_record')
        self.room_id = kwargs.get('room_id', '')
        self.create_time = kwargs.get('create_time', None)
        self.sender_code = kwargs.get('sender_code', '')
        self.message_content = kwargs.get('message_content', None)
        self.message_type = kwargs.get('message_type', '')

    @classmethod
    def init_chat_record(cls, **kwargs):
        chat_record = cls()
        chat_record.room_id = kwargs.get('room_id', '')
        chat_record.create_time = kwargs.get('create_time', None)
        chat_record.sender_code = kwargs.get('sender_code', '')
        chat_record.message_content = kwargs.get('message_content', None)
        chat_record.message_type = kwargs.get('message_type', '')
        return chat_record

    @try_except
    def send_message(self):
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self

    @try_except
    def get_chat_records_by_room_id(self, last_id=''):
        pipeline = []
        filter_list = [{'room_id': self.room_id}, ]
        if last_id:
            filter_list.append({'_id': {'$lt': ObjectId(last_id)}})

        pipeline.append({'$match': {'$and': filter_list}})
        pipeline.append({'$sort': {'_id': pymongo.DESCENDING}})

        pipeline.append({'$project': {
            '_id': {"$toString": "$_id"},
            'create_time': 1,
            'sender_code': 1,
            'message_content': 1,
            'message_type': 1
        }})
        return self.aggregate_by_pipeline(pipeline=pipeline)
