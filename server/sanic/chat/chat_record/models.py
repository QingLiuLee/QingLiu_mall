# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
from system.base_model import IBaseModel
from utils.decorator.exception import try_except


class ChatRecord(IBaseModel):
    __slots__ = (
        'room_id',
        'create_time',
        'is_org_room',
    )

    def __init__(self, **kwargs):
        super(ChatRecord, self).__init__('chat_record')
        self.room_id = kwargs.get('room_id', '')
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    def init_chat_room(cls, **kwargs):
        chat_room = cls()
        chat_room.room_id = kwargs.get('room_id', '')
        chat_room.create_time = kwargs.get('create_time', None)
        return chat_room
