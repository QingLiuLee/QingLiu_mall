# -*- coding: utf-8 -*-
# @Time     : 4/24/19 8:11 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from commodity.product.modes import Product
from system.response import *
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="product", url_prefix="/product", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_product_info(request: Request, token: Token):
    params = request.json

    category_code = params.get('category_code', '')
    product_name = params.get('product_name', '')
    org_code = params.get('org_code', '')
    img_list = params.get('img_list', '')
    explain = params.get('explain', '')
    sale_price = params.get('sale_price', '')

    if not all([category_code, product_name, org_code, img_list, explain, sale_price]):
        abort(status_code=ParamsErrorCode)

    product = Product.init_product_info(**params)
    is_exists = await product.find_info_by_org_code_and_product_name()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='产品信息已存在')

    product_code = product.create_product_info()
    if product_code:
        abort(status_code=JsonSuccessCode, message=product_code)

    abort(status_code=ServerErrorCode, message='产品创建失败')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_product_info(request: Request, token: Token):
    params = request.json

    org_code = params.get('org_code', '')
    product_code = params.get('product_code', '')
    product_name = params.get('product_name', '')
    img_list = params.get('img_list', '')
    explain = params.get('explain', '')
    sale_price = params.get('sale_price', '')

    if not all([org_code, product_code, product_name, img_list, explain, sale_price]):
        abort(status_code=ParamsErrorCode)

    product = Product.init_product_info(**params)

    old_product = await product.find_info_by_org_code_and_product_name()
    if old_product and old_product['product_code'] != product_code:
        abort(status_code=ExistsErrorCode, message='产品名已存在')

    result = await product.update_info_by_product_code()
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message=product_code)

    abort(status_code=ServerErrorCode, message='产品更新失败')


@blueprint.route(uri='/delete/info', methods=['POST'])
@response_exception
async def delete_product_info(request: Request, token: Token):
    """删除产品信息"""

    params = request.json

    product = Product.init_product_info(**params)
    if not product or not product.org_code:
        abort(status_code=ParamsErrorCode)

    product_list = await product.delete_info_by_product_code(product_code_list=params['product_code_list'])
    abort(status_code=JsonSuccessCode, message=product_list)


@blueprint.route(uri='/get/info/list', methods=['POST'])
@response_exception
async def get_product_info_list(request: Request, token: Token):
    """获取产品信息列表"""
    params = request.json

    limit = params.get('limit', 10)
    last_id = params.get('last_id', None)
    category_type = params.get('category_type', [])

    product = Product.init_product_info(**params)
    if not product or not product.org_code:
        abort(status_code=ParamsErrorCode)

    product_list = await product.find_product_list_by_org_code(category_type=category_type, limit=limit,
                                                               last_id=last_id)

    total_count = await product.get_all_product_count_by_org_code(category_type=category_type)

    for category in product_list:
        category['_id'] = str(category['_id'])

    abort(status_code=JsonSuccessCode, message={"list": product_list, "count": total_count})


@blueprint.route(uri='/drop/collection', methods=['POST'])
@response_exception
async def drop_collection(request: Request, token: Token):
    """删除商品collection"""

    product = Product()
    await product.drop_collection()
    abort(status_code=JsonSuccessCode, message='商品表已清除')
