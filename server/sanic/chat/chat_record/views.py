# -*- coding: utf-8 -*-
# @Time     : 2019/7/11
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from system.response import JsonSuccessCode, ParamsErrorCode, ServerErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="chat_record", url_prefix='/record', version=1)


@blueprint.route(uri='/get/record', methods=['POST'])
@response_exception
async def get_chat_room_record(request: Request, token: Token):
    """
    :name consumer_join_chat_room
    :param (consumer_code/room_id)
    """
    params = request.json

    # chat_room = ChatRoom.init_chat_room(**params)
    # if not params['consumer_code'] or not chat_room.room_id:
    #     abort(status_code=ParamsErrorCode)
    #
    # result = chat_room.consumer_join_chat_room(consumer_code=params['consumer_code'])
    # if result.modified_count:
    #     abort(status_code=JsonSuccessCode, message='join chat room success')
    #
    # abort(status_code=ServerErrorCode, message='join chat room failed')
