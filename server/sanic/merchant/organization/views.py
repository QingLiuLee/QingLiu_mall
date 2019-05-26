# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:13 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from merchant.organization.models import Organization
from merchant.staff.models import Staff
from system.response import BaseResponse
from utils.constant import ROLES
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="organization", url_prefix="/organization", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_org_info(request: Request, token: Token):
    """
    创建商家信息接口
    参数：staff_code
        org_name
        explain
        img_list
        sale_type
    """
    params = request.json
    response_data = BaseResponse()

    staff = Staff.init_staff_info(**params)
    staff_info = staff.get_staff_info_by_staff_code()

    if not staff_info:
        return response_data.set_system_error(message='所属管理员编码错误')

    org_obj = Organization.init_org_info(**params)
    if not all([org_obj, org_obj.check_params_is_none(except_list=['org_code', 'create_time'])]):
        return response_data.set_params_error()

    is_exist = await org_obj.find_org_by_org_name()
    if is_exist:
        return response_data.set_exist_error()

    org_code = org_obj.create_org_info()

    if org_code:

        await staff.set_org_roles_by_staff_code(org_code=org_code, role_code=ROLES['1'])

        return response_data.set_response_success(msg="{0} 商铺创建成功".format(org_obj.org_name))
    else:
        return response_data.set_system_error()


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_org_info(request: Request, token: Token):
    """更新商家信息"""
    params = request.json
    response_data = BaseResponse()

    org_code = params.get('org_code', '')
    org_name = params.get('org_name', '')
    explain = params.get('explain', '')
    img_list = params.get('img_list', [])
    sale_type = params.get('sale_type', [])
    owner_code = params.get('owner_code', '')

    if not all([org_code, org_name, explain, img_list, sale_type, owner_code]):
        return response_data.set_params_error()

    org_obj = Organization.init_org_info(**params)
    org_obj.update_merchant_info()

    return response_data.set_response_success(msg='更新成功')


@blueprint.route(uri='/get/info/list', methods=['POST'])
@response_exception
async def get_org_info_list(request: Request, token: Token):
    """根据管理员编码获取商家列表信息"""

    params = request.json
    response_data = BaseResponse()

    org_obj = Organization.init_org_info(**params)
    if not org_obj.staff_code:
        return response_data.set_params_error()

    org_list = await org_obj.find_all_org_list_by_staff_code()
    return response_data.set_response_success(data=org_list)
