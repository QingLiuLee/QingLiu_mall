# -*- coding: utf-8 -*-
# @Time     : 2019/7/10
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from chat.models import ChatRoom
from system.response import *
from utils.decorator.exception import try_except, response_exception
from system.extensions import socket_io

blueprint = Blueprint(name="chat", version=1)


@blueprint.route(uri='/into/chat/html', methods=['GET'])
@try_except
async def create_coupon_info(request: Request):
    """
    :name create_coupon_info
    :param ()
    """
    abort(status_code=HtmlSuccessCode, message='chat/chat.html')


@socket_io.event
async def join_room(socket_id, message):
    socket_io.enter_room(socket_id, message['room'])
    await socket_io.emit('my_response', {'data': 'Entered room: ' + message['room']},
                         room=socket_id)


@socket_io.event
async def leave_room(socket_id, message):
    socket_io.leave_room(socket_id, message['room'])
    await socket_io.emit('my_response', {'data': 'Left room: ' + message['room']},
                         room=socket_id)


@socket_io.event
async def close_room(socket_id, message):
    await socket_io.emit('my_response',
                         {'data': 'Room ' + message['room'] + ' is closing.'},
                         room=message['room'])
    await socket_io.close_room(message['room'])


@socket_io.event
async def room_chat_event(socket_id, message):
    await socket_io.emit(event=message['event'], data=message['data'], room=message['room_id'])


@socket_io.event
async def broadcast_event(socket_id, message):
    await socket_io.emit(event=message['event'], data=message['data'], room=message['room_id'])


@socket_io.event
async def disconnect_request(socket_id):
    await socket_io.disconnect(socket_id)


@socket_io.event
async def connect(socket_id, environ):
    await socket_io.emit('my_response', {'data': 'Connected', 'count': 0}, room=socket_id)


@socket_io.event
async def disconnect(socket_id):
    pass


@blueprint.route(uri='/get/chat/room/list', methods=['POST'])
@response_exception
async def get_consumer_chat_room_list(request: Request, token: Token):
    """
    :name get_consumer_chat_room_list
    :param (consumer_code)
    """
    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)

    if not params['consumer_code']:
        abort(status_code=ParamsErrorCode)

    chat_room_list = chat_room.get_chat_room_by_consumer_code(consumer_code=params['consumer_code'])
    abort(status_code=JsonSuccessCode, message={'chat_room_list': chat_room_list})


@blueprint.route(uri='/consumer/join/room', methods=['POST'])
@response_exception
async def consumer_join_chat_room(request: Request, token: Token):
    """
    :name consumer_join_chat_room
    :param (consumer_code/room_id)
    """
    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not params['consumer_code'] or not chat_room.room_id:
        abort(status_code=ParamsErrorCode)

    result = chat_room.consumer_join_chat_room(consumer_code=params['consumer_code'])
    if result.modified_count:
        abort(status_code=JsonSuccessCode, message='join chat room success')

    abort(status_code=ServerErrorCode, message='join chat room failed')


@blueprint.route(uri='/consumer/leave/room', methods=['POST'])
@response_exception
async def consumer_leave_chat_room(request: Request, token: Token):
    """
    :name consumer_leave_chat_room
    :param (consumer_code/room_id)
    """

    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not params['consumer_code'] or not chat_room.room_id:
        abort(status_code=ParamsErrorCode)

    result = chat_room.consumer_leave_chat_room(consumer_code=params['consumer_code'])
    if result.modified_count:
        abort(status_code=JsonSuccessCode, message='leave chat room success')

    abort(status_code=ServerErrorCode, message='leave chat room failed')


@blueprint.route(uri='/staff/join/room', methods=['POST'])
@response_exception
async def staff_join_chat_room(request: Request, token: Token):
    """
    :name staff_join_chat_room
    :param (staff_code/room_id)
    """

    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not params['staff_code'] and not chat_room.room_id:
        abort(status_code=ParamsErrorCode)

    result = chat_room.org_staff_join_chat_room(staff_code=params['staff_code'])
    if result.modified_count:
        abort(status_code=JsonSuccessCode, message='join chat room success')

    abort(status_code=ServerErrorCode, message='join chat room failed')


@blueprint.route(uri='/staff/leave/room', methods=['POST'])
@response_exception
async def staff_leave_chat_room(request: Request, token: Token):
    """
    :name staff_leave_chat_room
    :param (staff_code/room_id)
    """

    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not params['staff_code'] or not chat_room.room_id:
        abort(status_code=ParamsErrorCode)

    result = chat_room.org_staff_join_chat_room(staff_code=params['staff_code'])
    if result.modified_count:
        abort(status_code=JsonSuccessCode, message='leave chat room success')

    abort(status_code=ServerErrorCode, message='leave chat room failed')
