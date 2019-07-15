# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from chat.chat_room.models import ChatRoom
from system.response import ParamsErrorCode, JsonSuccessCode, ServerErrorCode, ExistsErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="chat_room", url_prefix='/room', version=1)


@blueprint.route(uri='/consumer/get/rooms', methods=['POST'])
@response_exception
async def consumer_get_chat_rooms(request: Request, token: Token):
    """
    :name consumer_get_chat_rooms
    :param (consumer_code)
    """
    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not params['consumer_code']:
        abort(status_code=ParamsErrorCode)

    chat_room_list = await chat_room.get_chat_rooms_by_consumer_code(consumer_code=params['consumer_code'])
    abort(status_code=JsonSuccessCode, message={'chat_room_list': chat_room_list})


@blueprint.route(uri='/consumer/create/room', methods=['POST'])
@response_exception
async def consumer_create_chat_room(request: Request, token: Token):
    """
    :name consumer_create_chat_room
    :param (consumer_code_list/admin_code/is_group/room_name)
    """
    params = request.json

    chat_room = ChatRoom.init_chat_room(**params)
    if not chat_room.check_params_is_none(['room_id', 'is_org_room', 'org_staff_code_list',
                                           'create_time', 'org_code', 'room_event']):
        abort(status_code=ParamsErrorCode)

    chat_room.consumer_create_chat_room()
    abort(status_code=JsonSuccessCode, message='consumer chat room create success')


@blueprint.route(uri='/consumer/join/room', methods=['POST'])
@response_exception
async def consumer_join_chat_room(request: Request, token: Token):
    """
    :name consumer_join_chat_room
    :param (consumer_code/room_id)
    """

    params = request.json
    chat_room = ChatRoom.init_chat_room(**params)
    if not params['consumer_code'] or not params['room_id']:
        abort(status_code=ParamsErrorCode)

    is_exists = await chat_room.consumer_get_chat_room_by_code_and_id(consumer_code=params['consumer_code'])
    if is_exists:
        abort(status_code=ExistsErrorCode, message='the consumer already exists')

    await chat_room.consumer_join_chat_room(consumer_code=params['consumer_code'])
    abort(status_code=JsonSuccessCode, message='the consumer join room success')


@blueprint.route(uri='/consumer/leave/room', methods=['POST'])
@response_exception
async def consumer_leave_chat_room(request: Request, token: Token):
    """
    :name consumer_leave_chat_room
    :param (consumer_code/room_id)
    """

    params = request.json
    chat_room = ChatRoom.init_chat_room(**params)
    if not params['consumer_code'] or not params['room_id']:
        abort(status_code=ParamsErrorCode)

    await chat_room.consumer_leave_chat_room(consumer_code=params['consumer_code'])
    abort(status_code=JsonSuccessCode, message='the consumer leave chat room success')
