# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:06 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.integral_detail.models import IntegralDetail, IntegralHistoryInfo
from system.response import ServerErrorCode, JsonSuccessCode, ExistsErrorCode, ParamsErrorCode, NoExistsErrorCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="integral_detail", url_prefix='/integral_detail', version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_integral_detail_info(request: Request, token: Token):
    """
    :name create_task_detail_info
    :param (consumer_code)
    """

    params = request.json
    integral_detail = IntegralDetail.init_integral_detail(**params)
    if not integral_detail.consumer_code:
        abort(status_code=ParamsErrorCode)

    detail_info = await integral_detail.get_integral_detail_by_consumer_code()
    if detail_info:
        abort(status_code=ExistsErrorCode, message='the task already exists.')

    total_integral = integral_detail.create_integral_detail_info()
    abort(status_code=JsonSuccessCode, message={'total_integral': total_integral})


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_integral_detail_info(request: Request, token: Token):
    """
    :name update_task_detail_info
    :param (consumer_code, income_type, integral_value, detail)
    """

    params = request.json

    integral_detail = IntegralDetail.init_integral_detail(**params)
    history_info = IntegralHistoryInfo.init_history_info(**params)

    if not all([integral_detail.consumer_code, history_info.check_params_is_none(['create_time'])]):
        abort(status_code=ParamsErrorCode)

    detail_info = await integral_detail.get_integral_detail_by_consumer_code()
    if not detail_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    if history_info.income_type > 0:
        integral_value = 1 * float(history_info.integral_value)
    elif history_info.income_type < 0:
        integral_value = -1 * float(history_info.integral_value)
    else:
        integral_value = 0

    result = await integral_detail.update_consumer_integral_detail(integral_value=integral_value,
                                                                   history_info=history_info)

    if result.modified_count:
        abort(status_code=JsonSuccessCode, message='update integral detail success')

    abort(status_code=ServerErrorCode, message='update integral detail failed')
