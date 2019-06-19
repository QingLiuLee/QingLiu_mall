# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:10 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from system.response import ParamsErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="vip", url_prefix='/vip', version=1)


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

    # consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
    pass
