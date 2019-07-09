# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.integral_detail.models import ConsumerIntegralDetail
from system.response import *
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="integral_detail", url_prefix='/integral_detail', version=1)


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_integral_detail_info(request: Request, token: Token):
    """
    :name get_integral_detail_info
    :param (consumer_code)
    """

    params = request.json
    integral_detail = ConsumerIntegralDetail.init_integral_detail(**params)
    if not integral_detail.consumer_code:
        abort(status_code=ParamsErrorCode)

    detail_info = await integral_detail.get_integral_detail_by_consumer_code()
    if not detail_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    detail_info['_id'] = str(detail_info['_id'])

    abort(status_code=JsonSuccessCode, message={'detail_info': detail_info})
