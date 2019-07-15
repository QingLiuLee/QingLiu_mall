# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.order_detail.models import ConsumerOrderDetail
from system.response import ParamsErrorCode, NoExistsErrorCode, JsonSuccessCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="order_detail", url_prefix='/order_detail', version=1)


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_order_detail_info(request: Request, token: Token):
    """
    :name get_order_detail_info
    :param (consumer_code)
    """

    params = request.json
    order_detail = ConsumerOrderDetail.init_order_detail(**params)
    if not order_detail.consumer_code:
        abort(status_code=ParamsErrorCode)

    detail_info = await order_detail.get_order_detail_by_consumer_code()
    if not detail_info:
        abort(status_code=NoExistsErrorCode, message='the order detail no exists.')

    abort(status_code=JsonSuccessCode, message={'order_detail': detail_info})
