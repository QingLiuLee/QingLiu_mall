# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from commodity.category.models import Category
from system.response import BaseResponse
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="category", url_prefix="/category", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_category_info(request: Request, token: Token):
    params = request.json
    response_data = BaseResponse()

    category_name = params.get('category_name', '')
    merchant_code = params.get('merchant_code', '')

    if not all([category_name, merchant_code]):
        return response_data.set_params_error()

    category = Category.init_category_info(**params)

    is_exists = category.find_category_by_merchant_code_and_category_name()
    if is_exists:
        return response_data.set_exist_error()

    category_code = category.create_category_info()

    if category_code:
        return response_data.set_response_success(msg='品类创建成功')

    return response_data.set_system_error(message='新增品类失败')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_category_info(request: Request, token: Token):
    params = request.json
    response_data = BaseResponse()

    category_name = params.get('category_name', '')
    category_code = params.get('category_code', '')
    merchant_code = params.get('merchant_code', '')
    if not all([category_name, category_code, merchant_code]):
        return response_data.set_params_error()

    category = Category.init_category_info(**params)

    is_exists = category.find_category_by_merchant_code_and_category_name()
    if is_exists:
        return response_data.set_exist_error()

    result = await category.update_category_info()

    if result.modified_count or result.matched_count:
        return response_data.set_response_success()

    return response_data.set_system_error(message='更新失败')
