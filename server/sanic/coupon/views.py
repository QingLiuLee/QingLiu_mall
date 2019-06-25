# -*- coding: utf-8 -*-
# @Time     : 6/17/19 7:23 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from coupon.models import Coupon
from system.response import ParamsErrorCode, ExistsErrorCode, JsonSuccessCode, ServerErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="coupon", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_coupon_info(request: Request, token: Token):
    """create coupon info"""
    params = request.json

    title = params.get('title', '')
    start_time = params.get('start_time', None)
    end_time = params.get('end_time', None)
    explain = params.get('explain', '')
    total_num = params.get('total_num', '')
    distribution_form_type = params.get('distribution_form_type', '')
    distribution_form_value = params.get('distribution_form_value', '')
    use_threshold = params.get('use_threshold', '')
    available_product_type = params.get('available_product_type', [])
    available_product_list = params.get('available_product_list', [])
    limit_num = params.get('limit_num', 0)
    consumer_type = params.get('consumer_type', '')
    consumer_value = params.get('consumer_value', [])

    coupon = Coupon.init_coupon_info(**params)

    if not all(coupon.check_params_is_none(['coupon_code', 'create_time', 'used_num', 'received_num'
                                                                                      'vail_status'])):
        abort(status_code=ParamsErrorCode)

    is_exists = await coupon.find_coupon_by_title()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='优惠券标题已存在')

    coupon_code = coupon.create_coupon_info()
    if coupon_code:
        abort(status_code=JsonSuccessCode, message={'coupon_code': coupon_code})

    abort(status_code=ServerErrorCode, message='优惠券创建失败')
