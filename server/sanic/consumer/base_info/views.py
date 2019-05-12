# -*- coding: utf-8 -*-
# @Time     : 5/6/19 7:02 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from bson import json_util
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.base_info.models import ConsumerBaseInfo, Consumer, ReceivingAddress
from system.response import BaseResponse
from sanic_jwt_extended import create_access_token

from utils.decorator.exception import response_exception

blueprint = Blueprint(name="base_info", url_prefix='/base_info', version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
async def create_consumer_info(request):
    params = request.json
    response_data = BaseResponse()
    try:

        base_info = ConsumerBaseInfo.init_base_info(**params)

        if not base_info.check_params_is_none():
            return response_data.set_params_error()

        consumer = Consumer.init_consumer_info(base_info=base_info)
        old_info = await consumer.find_consumer_by_mobile_or_nickname()
        if old_info:
            return response_data.set_exist_error()

        consumer_code = consumer.create_consumer_info()

        if consumer_code:
            return response_data.set_response_success()
        else:
            return response_data.set_system_error()
    except Exception as e:
        return response_data.set_system_error(message=e)


@blueprint.route(uri='/sign/in', methods=['POST'])
async def consumer_sign_in(request):
    """消费者登录接口"""

    params = request.json
    response_data = BaseResponse()

    try:
        account = params.get('account', '')
        password = params.get('password', '')

        if not all([account, password]):
            return response_data.set_params_error()

        base_info = ConsumerBaseInfo.init_base_info(**params)

        consumer = Consumer.init_consumer_info(base_info=base_info)

        consumer_info = await consumer.find_consumer_by_mobile_or_nickname()
        if not consumer_info:
            return response_data.set_no_exist_error()

        consumer = consumer.init_consumer_info(**consumer_info)
        if consumer.check_consumer_password(password):
            token = await create_access_token(app=request.app, identity='nickname',
                                              user_claims=json_util.dumps(consumer_info))
            return response_data.set_response_success(data=token)
        else:
            return response_data.identity_authentication_error()

    except Exception as e:
        return response_data.set_system_error(message=e)


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_consumer_base_info(request: Request, token: Token):
    """获取消费者的基本信息"""
    params = request.json
    response_data = BaseResponse()

    mobile = params.get('mobile', '')
    nickname = params.get('nickname', '')

    if not mobile and not nickname:
        return response_data.set_params_error()

    base_info = ConsumerBaseInfo.init_base_info(**params)
    consumer = Consumer.init_consumer_info(base_info=base_info.get_json_by_obj())
    consumer_info = await consumer.find_consumer_by_mobile_or_nickname()

    if not consumer_info:
        return response_data.set_no_exist_error()

    return response_data.set_response_success(data=consumer_info)


@blueprint.route(uri='/update/vip/info', methods=['POST'])
@response_exception
async def update_vip_info(request: Request, token: Token):
    """更新消费者ＶＩＰ信息中的等级信息"""
    params = request.json
    response_data = BaseResponse()

    consumer_code = params.get('consumer_code', '')
    old_vip_level = params.get('old_vip_level', '')
    new_vip_level = params.get('new_vip_level', '')

    if not all([consumer_code, old_vip_level, new_vip_level]):
        return response_data.set_params_error()

    consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
    pass


@blueprint.route(uri='/add/receive/address', methods=['POST'])
@response_exception
async def add_consumer_receive_address(request: Request, token: Token):
    """添加消费者收货地址"""

    params = request.json
    response_data = BaseResponse()

    receive_address = ReceivingAddress.init_receiving_address(**params)
    if not all([receive_address, receive_address.check_params_is_none()]):
        return response_data.set_params_error()

    consumer_code = params.get('consumer_code', '')
    consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
    result = consumer.add_consumer_receive_address(receive_address)

    return response_data.set_response_success()
