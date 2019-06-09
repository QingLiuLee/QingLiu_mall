# -*- coding: utf-8 -*-
# @Time     : 5/6/19 7:02 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from bson import json_util
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.base_info.models import ConsumerBaseInfo, Consumer, ReceivingAddress
from system.response import *
from sanic_jwt_extended import create_access_token

from utils.decorator.exception import response_exception

blueprint = Blueprint(name="base_info", url_prefix='/base_info', version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
async def create_consumer_info(request):
    params = request.json
    base_info = ConsumerBaseInfo.init_base_info(**params)

    if not base_info.check_params_is_none():
        abort(status_code=ParamsErrorCode)

    consumer = Consumer.init_consumer_info(base_info=base_info)
    old_info = await consumer.find_consumer_by_mobile_or_nickname()
    if old_info:
        abort(status_code=ExistsErrorCode, message='账号已存在')

    consumer_code = consumer.create_consumer_info()

    if consumer_code:
        abort(status_code=JsonSuccessCode, message=consumer_code)
    else:
        abort(status_code=ServerErrorCode, message='账号创建失败')


@blueprint.route(uri='/sign/in', methods=['POST'])
async def consumer_sign_in(request):
    """消费者登录接口"""

    params = request.json

    account = params.get('account', '')
    password = params.get('password', '')

    if not all([account, password]):
        abort(status_code=ParamsErrorCode)

    base_info = ConsumerBaseInfo.init_base_info(**params)

    consumer = Consumer.init_consumer_info(base_info=base_info)

    consumer_info = await consumer.find_consumer_by_mobile_or_nickname()
    if not consumer_info:
        abort(status_code=NoExistsErrorCode, message='当前账号不存在')

    consumer = consumer.init_consumer_info(**consumer_info)
    if consumer.check_consumer_password(password):
        token = await create_access_token(app=request.app, identity='nickname',
                                          user_claims=json_util.dumps(consumer_info))

        abort(status_code=JsonSuccessCode, message={'token': token})
    else:
        abort(status_code=UnAuthorizedCode, message='账号或密码错误')


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_consumer_base_info(request: Request, token: Token):
    """获取消费者的基本信息"""
    params = request.json

    mobile = params.get('mobile', '')
    nickname = params.get('nickname', '')

    if not mobile and not nickname:
        abort(status_code=ParamsErrorCode)

    base_info = ConsumerBaseInfo.init_base_info(**params)
    consumer = Consumer.init_consumer_info(base_info=base_info.get_json_by_obj())
    consumer_info = await consumer.find_consumer_by_mobile_or_nickname()

    if not consumer_info:
        abort(status_code=NoExistsErrorCode, message='当前账号不存在')

    abort(status_code=JsonSuccessCode, message=consumer_info)


@blueprint.route(uri='/update/vip/info', methods=['POST'])
@response_exception
async def update_vip_info(request: Request, token: Token):
    """更新消费者ＶＩＰ信息中的等级信息"""
    params = request.json

    consumer_code = params.get('consumer_code', '')
    old_vip_level = params.get('old_vip_level', '')
    new_vip_level = params.get('new_vip_level', '')

    if not all([consumer_code, old_vip_level, new_vip_level]):
        abort(status_code=ParamsErrorCode)

    consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
    pass


@blueprint.route(uri='/add/receive/address', methods=['POST'])
@response_exception
async def add_consumer_receive_address(request: Request, token: Token):
    """添加消费者收货地址"""

    params = request.json

    receive_address = ReceivingAddress.init_receiving_address(**params)
    if not all([receive_address, receive_address.check_params_is_none()]):
        abort(status_code=ParamsErrorCode)

    consumer_code = params.get('consumer_code', '')
    consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
    result = consumer.add_consumer_receive_address(receive_address)

    abort(status_code=JsonSuccessCode)
