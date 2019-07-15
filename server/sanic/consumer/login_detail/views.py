# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.login_detail.models import ConsumerLoginDetail
from system.response import ParamsErrorCode, NoExistsErrorCode, JsonSuccessCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="login_detail", url_prefix='/login_detail', version=1)


@blueprint.route(uri='/get/login_history', methods=['POST'])
@response_exception
async def get_consumer_login_history(request: Request, token: Token):
    """创建消费者账号信息"""
    """参数(consumer_code)"""
    params = request.json
    consumer = ConsumerLoginDetail.init_login_detail(**params)

    if not consumer.consumer_code:
        abort(status_code=ParamsErrorCode)

    login_history = await consumer.get_login_history_by_consumer_code()
    if not login_history:
        abort(status_code=NoExistsErrorCode, message='the consumer login detail no exists')

    abort(status_code=JsonSuccessCode, message={'login_history': login_history['login_history']})
