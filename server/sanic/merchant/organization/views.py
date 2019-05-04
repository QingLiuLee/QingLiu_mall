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
    :param request:
    :return:
    """
    params = request.json
    response_data = BaseResponse()

    merchant_name = params.get('merchant_name', '')
    explain = params.get('explain', '')
    img_list = params.get('img_list', [])
    sale_type = params.get('sale_type', [])
    owner_code = params.get('owner_code', '')

    if not all([merchant_name, img_list, sale_type, owner_code]):
        return response_data.set_params_error()

    staff = Staff.init_staff_info(staff_code=owner_code)

    if not staff:
        return response_data.set_system_error(message='所属管理员编码错误')

    org_obj = Organization.init_org_info(**params)

    is_exist = await org_obj.find_org_by_merchant_name(merchant_name=merchant_name)
    if is_exist:
        return response_data.set_exist_error()

    org_code = org_obj.create_org_info()

    if org_code:

        await staff.set_org_roles_by_staff_code(org_code=org_code, role_code=ROLES['1'])

        return response_data.set_response_success(msg="{0} 商铺创建成功".format(merchant_name))
    else:
        return response_data.set_system_error()
