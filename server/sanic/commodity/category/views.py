# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from commodity.category.models import Category
from system.response import *
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

    category = Category.init_category_info(**params)
    if not category.check_params_is_none(['category_code', 'create_time']):
        abort(status_code=ParamsErrorCode)

    is_exists = await category.find_category_by_org_code_and_category_name()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='商家品类信息已存在')

    category_code = category.create_category_info()

    if category_code:
        abort(status_code=JsonSuccessCode, message=category_code)
    abort(status_code=ServerErrorCode, message='商家品类创建失败')


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

    category = Category.init_category_info(**params)
    if not all([category, category.check_params_is_none(['create_time'])]):
        abort(status_code=ParamsErrorCode)

    old_category = await category.find_category_by_org_code_and_category_name()
    if old_category and old_category['category_code'] != category.category_code:
        abort(status_code=ExistsErrorCode, message='品类信息已存在')

    result = await category.update_category_info()

    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message='品类更新成功')

    abort(status_code=ServerErrorCode, message='品类更新失败')


@blueprint.route(uri='/get/info/list', methods=['POST'])
@response_exception
async def get_category_info_list(request: Request, token: Token):
    """
    获取商家创建的品类列表
    参数:org_code
    """

    params = request.json

    limit = params.get('limit', 10)
    last_id = params.get('last_id', None)

    category = Category.init_category_info(**params)
    if not category or not category.org_code:
        abort(status_code=ParamsErrorCode)

    category_list = await category.find_category_list_by_org_code(limit=limit, last_id=last_id)
    total_count = await category.get_all_category_count_by_org_code()

    for category in category_list:
        category['_id'] = str(category['_id'])

    abort(status_code=JsonSuccessCode, message={"list": category_list, "count": total_count})


@blueprint.route(uri='/delete/info', methods=['POST'])
@response_exception
async def delete_category_info(request: Request, token: Token):
    """删除商家的品类信息"""

    params = request.json

    category = Category.init_category_info(**params)
    if not category or not category.org_code:
        abort(status_code=ParamsErrorCode)

    category_list = await category.delete_category_by_org_code_and_category_code_list(
        category_code_list=params['category_code_list'])
    abort(status_code=JsonSuccessCode, message=category_list)


@blueprint.route(uri='/drop/collection', methods=['POST'])
@response_exception
async def drop_collection(request: Request, token: Token):
    """删除品类collection"""

    category = Category()
    await category.drop_collection()
    abort(status_code=JsonSuccessCode, message='品类表已清除')
