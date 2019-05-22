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
    """
    商家创建品类信息
    参数：category_name:
         staff_code
         org_code
    """
    params = request.json
    response_data = BaseResponse()

    category = Category.init_category_info(**params)
    if not category.check_params_is_none(['category_code', 'create_time']):
        return response_data.set_params_error()

    is_exists = await category.find_category_by_org_code_and_category_name()
    if is_exists:
        return response_data.set_exist_error()

    category_code = category.create_category_info()

    if category_code:
        return response_data.set_response_success(msg='品类创建成功')

    return response_data.set_system_error(message='品类创建失败')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_category_info(request: Request, token: Token):
    """
    更新品类信息
    参数：category_name
         category_code
         org_code
         staff_code
    """
    params = request.json
    response_data = BaseResponse()

    category = Category.init_category_info(**params)
    if not all([category, category.check_params_is_none([category.create_time])]):
        return response_data.set_params_error()

    is_exists = category.find_category_by_org_code_and_category_name()
    if is_exists:
        return response_data.set_exist_error()

    result = await category.update_category_info()

    if result.modified_count or result.matched_count:
        return response_data.set_response_success(msg='品类更新成功')

    return response_data.set_system_error(message='品类更新失败')


@blueprint.route(uri='/get/info/list', methods=['POST'])
@response_exception
async def get_category_info_list(request: Request, token: Token):
    """
    获取商家创建的品类列表
    参数:org_code
    """

    params = request.json
    response_data = BaseResponse()

    category = Category.init_category_info(**params)
    if not category or not category.org_code:
        return response_data.set_params_error()

    category_list = await category.find_category_list_by_org_code()
    return response_data.set_response_success(data=category_list)
