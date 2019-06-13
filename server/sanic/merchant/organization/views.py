# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:13 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from merchant.organization.models import Organization
from merchant.staff.models import Staff
from system.response import *
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

    staff = Staff.init_staff_info(**params)
    staff_info = staff.get_staff_info_by_staff_code()

    if not staff_info:
        abort(status_code=NoExistsErrorCode, message='当前账号不存在')

    org_obj = Organization.init_org_info(**params)
    if not all([org_obj, org_obj.check_params_is_none(except_list=['org_code', 'create_time'])]):
        abort(status_code=ParamsErrorCode)

    is_exist = await org_obj.find_org_by_org_name()
    if is_exist:
        abort(status_code=ExistsErrorCode, message='商家已存在')

    org_code = org_obj.create_org_info()

    if org_code:

        await staff.set_org_roles_by_staff_code(org_code=org_code, role_code=ROLES['1'])
        abort(status_code=JsonSuccessCode, message=org_obj.org_code)
    else:
        abort(status_code=ServerErrorCode, message='商家创建失败')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_org_info(request: Request, token: Token):
    """更新商家信息"""
    params = request.json

    org_obj = Organization.init_org_info(**params)
    if not org_obj.check_params_is_none():
        abort(status_code=ParamsErrorCode)
        
    org_obj.update_merchant_info()
    abort(status_code=JsonSuccessCode, message='更新成功')


@blueprint.route(uri='/get/info/list', methods=['POST'])
@response_exception
async def get_org_info_list(request: Request, token: Token):
    """根据管理员编码获取商家列表信息"""

    params = request.json

    org_obj = Organization.init_org_info(**params)
    if not org_obj.staff_code:
        abort(status_code=ParamsErrorCode)

    org_list = await org_obj.find_all_org_list_by_staff_code()
    abort(status_code=JsonSuccessCode, message=org_list)
