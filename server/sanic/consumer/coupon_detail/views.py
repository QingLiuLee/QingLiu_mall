# -*- coding: utf-8 -*-
# @Time     : 2019/7/9
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.coupon_detail.models import ConsumerCouponDetail
from system.response import ParamsErrorCode, NoExistsErrorCode, JsonSuccessCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="coupon_detail", url_prefix='/coupon_detail', version=1)


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_coupon_detail_info(request: Request, token: Token):
    """
    :name get_coupon_detail_info
    :param (consumer_code)
    """

    params = request.json
    coupon_detail = ConsumerCouponDetail.init_coupon_detail(**params)
    if not coupon_detail.consumer_code:
        abort(status_code=ParamsErrorCode)

    detail_info = await coupon_detail.get_coupon_detail_by_consumer_code()
    if not detail_info:
        abort(status_code=NoExistsErrorCode, message='the coupon detail no exists.')

    abort(status_code=JsonSuccessCode, message={'coupon_detail': detail_info})
