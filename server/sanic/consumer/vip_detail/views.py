# -*- coding: utf-8 -*-
# @Time     : 6/14/19 4:10 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.vip_detail.models import ConsumerVIPDetail
from system.response import ParamsErrorCode, NoExistsErrorCode, JsonSuccessCode
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="vip_detail", url_prefix='/vip_detail', version=1)


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_vip_detail_info(request: Request, token: Token):
    """
    :name get_task_detail_info
    :param (consumer_code)
    """

    params = request.json
    vip_detail = ConsumerVIPDetail.init_vip_detail(**params)
    if not vip_detail.consumer_code:
        abort(status_code=ParamsErrorCode)

    detail_info = await vip_detail.get_vip_detail_by_consumer_code()
    if not detail_info:
        abort(status_code=NoExistsErrorCode, message='the vip detail no exists.')

    abort(status_code=JsonSuccessCode, message={'vip_detail': detail_info})


# @blueprint.route(uri='/update/vip/info', methods=['POST'])
# @response_exception
# async def update_vip_info(request: Request, token: Token):
#     """更新消费者ＶＩＰ信息中的等级信息"""
#     params = request.json
#
#     consumer_code = params.get('consumer_code', '')
#     old_vip_level = params.get('old_vip_level', '')
#     new_vip_level = params.get('new_vip_level', '')
#
#     if not all([consumer_code, old_vip_level, new_vip_level]):
#         abort(status_code=ParamsErrorCode)
#
#     # consumer = Consumer.init_consumer_info(consumer_code=consumer_code)
#     pass
