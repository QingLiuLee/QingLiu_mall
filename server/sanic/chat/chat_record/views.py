# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from chat.chat_record.models import ChatRecord
from chat.chat_room.models import ChatRoom
from system.extensions import socket_io
from system.response import JsonSuccessCode, ParamsErrorCode, ServerErrorCode, NoExistsErrorCode
from utils.constant import MESSAGE_TYPE
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="chat_record", url_prefix='/record', version=1)


@blueprint.route(uri='/get/records', methods=['POST'])
@response_exception
async def consumer_get_chat_room_record(request: Request, token: Token):
    """
    :name consumer_get_chat_room_record
    :param (consumer_code/room_id/last_id)
    """
    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    chat_record = ChatRecord.init_chat_record(**params)
    if not params['consumer_code'] or not chat_room.room_id:
        abort(status_code=ParamsErrorCode)

    chat_room_info = chat_room.consumer_get_chat_room_by_code_and_id(consumer_code=params['consumer_code'])
    if not chat_room_info:
        abort(status_code=NoExistsErrorCode, message='the consumer not exists chat room')

    record_list = await chat_record.get_chat_records_by_room_id(params['last_id'])

    abort(status_code=JsonSuccessCode, message={'chat_record_list': record_list})


@blueprint.route(uri='/consumer/send/message', methods=['POST'])
@response_exception
async def consumer_send_message(request: Request, token: Token):
    """
    :name consumer_send_message
    :param (room_id/sender_code/message_content/)
    """
    params = request.json
    room_id = params['room_id']

    chat_record = ChatRecord.init_chat_record(**params)
    chat_room = ChatRoom.init_chat_room(**params)
    if not chat_record.check_params_is_none(['create_time', 'message_type']):
        abort(status_code=ParamsErrorCode)

    chat_room_info = await chat_room.consumer_get_chat_room_by_code_and_id(consumer_code=params['sender_code'])
    if not chat_room_info:
        abort(status_code=NoExistsErrorCode, message='the consumer not exists chat room')

    chat_record.send_message()

    await socket_io.emit(chat_room_info['room_event'], {'message_content': params['message_content']},
                         room=room_id)
    abort(status_code=JsonSuccessCode, message='the message send success')
