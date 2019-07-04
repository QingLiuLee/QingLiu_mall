# -*- coding: utf-8 -*-
# @Time     : 2019/7/3
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from integral.models import Integral
from system.response import ParamsErrorCode, ExistsErrorCode, JsonSuccessCode, ServerErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="integral", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_integral_info(request: Request, token: Token):
    """
    :name create_integral_info
    :param (integral_value/explain)
    """

    params = request.json

    integral = Integral.init_integral_info(**params)

    if not all(integral.check_params_is_none(['integral_code', 'create_time'])):
        abort(status_code=ParamsErrorCode)

    is_exists = await integral.find_integral_by_value()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='the integral already exists.')

    integral_code = integral.create_integral_info()
    if integral_code:
        abort(status_code=JsonSuccessCode, message={'integral_code': integral_code})

    abort(status_code=ServerErrorCode, message='create the integral failed.')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_integral_info(request: Request, token: Token):
    """
    :name update_integral_info
    :param (integral_code/integral_value/explain)
    """

    params = request.json
    integral = Integral.init_integral_info(**params)

    if not all(integral.check_params_is_none(['create_time'])):
        abort(status_code=ParamsErrorCode)

    is_exists = integral.find_integral_by_value()
    if is_exists and is_exists['integral_code'] != integral.integral_code:
        abort(status_code=ExistsErrorCode, message='the integral already exists.')

    result = integral.update_integral_info()
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message='the integral update success')

    abort(status_code=ServerErrorCode, message='the integral update failed')


@blueprint.route(uri='/delete/info', methods=['POST'])
@response_exception
async def delete_integral_info(request: Request, token: Token):
    """
    :name delete_integral_info
    :param (integral_code)
    """
    params = request.json
    integral = Integral.init_integral_info(**params)

    if not integral.integral_code:
        abort(status_code=ParamsErrorCode)

    result = integral.delete_integral_info()
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message='the integral update success')

    abort(status_code=ServerErrorCode, message='the integral update failed')
