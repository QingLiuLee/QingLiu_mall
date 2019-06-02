# -*- coding: utf-8 -*-
# @Time     : 4/24/19 8:11 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from commodity.product.modes import Product
from system.response import BaseResponse
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="product", url_prefix="/product", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_product_info(request: Request, token: Token):
    params = request.json
    response_data = BaseResponse()

    category_code = params.get('category_code', '')
    product_name = params.get('product_name', '')
    org_code = params.get('org_code', '')
    img_list = params.get('img_list', '')
    explain = params.get('explain', '')
    sale_price = params.get('sale_price', '')

    if not all([category_code, product_name, org_code, img_list, explain, sale_price]):
        return response_data.set_params_error()

    product = Product.init_product_info(**params)
    is_exists = await product.find_info_by_org_code_and_product_name()
    if is_exists:
        return response_data.set_exist_error()

    product_code = product.create_product_info()
    if product_code:
        return response_data.set_response_success()

    return response_data.set_system_error()


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_product_info(request: Request, token: Token):
    params = request.json
    response_data = BaseResponse()

    org_code = params.get('org_code', '')
    product_code = params.get('product_code', '')
    product_name = params.get('product_name', '')
    img_list = params.get('img_list', '')
    explain = params.get('explain', '')
    sale_price = params.get('sale_price', '')

    if not all([org_code, product_code, product_name, img_list, explain, sale_price]):
        return response_data.set_params_error()

    product = Product.init_product_info(**params)

    result = await product.update_info_by_product_code()
    if result.modified_count or result.matched_count:
        return response_data.set_response_success()

    return response_data.set_system_error(message='更新失败')


@blueprint.route(uri='/delete/info', methods=['POST'])
@response_exception
async def delete_product_info(request: Request, token: Token):
    """删除产品信息"""

    params = request.json
    response_data = BaseResponse()

    product = Product.init_product_info(**params)
    if not product or product.org_code:
        return response_data.set_params_error()

    product_list = await product.delete_info_by_product_code(product_code_list=params['product_code_list'])
    return response_data.set_response_success(data=product_list)
