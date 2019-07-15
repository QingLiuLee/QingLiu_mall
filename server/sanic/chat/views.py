# -*- coding: utf-8 -*-
# @Time     : 2019/7/10
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request

from chat.chat_room.models import ChatRoom
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
async def join_room(sid, message):
    rooms = socket_io.rooms(sid)
    if message['room'] not in rooms:
        socket_io.enter_room(sid, message['room'])
    await socket_io.emit('join_room', {'data': 'Entered room: ' + message['room']},
                         room=sid)


@socket_io.event
async def leave_room(sid, message):
    socket_io.leave_room(sid, message['room'])
    await socket_io.emit('my_response', {'data': 'Left room: ' + message['room']},
                         room=sid)


@socket_io.event
async def close_room(sid, message):
    await socket_io.emit('my_response',
                         {'data': 'Room ' + message['room'] + ' is closing.'},
                         room=message['room'])
    await socket_io.close_room(message['room'])


@socket_io.event
async def my_event(sid, message):
    await socket_io.emit('my_response', {'data': message['data']}, room=sid)


# @socket_io.event
# async def my_broadcast_event(sid, message):
#     await socket_io.emit('my_response', {'data': message['data']})


@socket_io.event
async def my_room_event(sid, message):
    await socket_io.emit('my_response', {'data': message['data']},
                         room=message['room'])


@socket_io.event
async def disconnect_request(sid):
    await socket_io.disconnect(sid)


@socket_io.event
async def connect(sid, query_params):
    """
    get client connect
    获取当前用户的全部房间并join
    """
    params_dict = {}
    query_params = query_params['QUERY_STRING'].split('&')
    for param in query_params:
        p = param.split('=')
        params_dict[p[0]] = p[1] if len(p) == 2 else ''

    if 'consumer_code' in params_dict.keys():

        chat_room = ChatRoom.init_chat_room()

        room_id_list = await chat_room.get_rooms_id_by_consumer_code(consumer_code=params_dict['consumer_code'])
        for room_info in room_id_list:
            socket_io.enter_room(sid, room_info['room_id'])

    await socket_io.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
