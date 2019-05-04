# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe :
from bson import json_util
from sanic import Blueprint
from sanic_jwt_extended import create_access_token

from merchant.staff.models import Staff
from system.response import BaseResponse
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="staff", url_prefix="/staff", version=1)


@blueprint.route(uri='/create/administrators/info', methods=['POST'])
async def create_admin_info(request):
    params = request.json
    response_data = BaseResponse()
    try:

        mobile = params.get('mobile', '')
        nickname = params.get('nickname', '')
        password = params.get('password', '')

        if not all([mobile, nickname, password]):
            response_data.set_params_error()

        staff = Staff()
        staff_info = await staff.find_staff_by_mobile_or_nickname(mobile=mobile, nickname=nickname)
        if staff_info:
            return response_data.set_exist_error()

        staff = staff.init_staff_info(mobile=mobile, nickname=nickname, password=password)
        staff_code = staff.create_admin_info()

        if staff_code:
            return response_data.set_response_success()
        else:
            return response_data.set_system_error()
    except Exception as e:
        return response_data.set_system_error(message=e)


@blueprint.route(uri='/sign/in', methods=['POST'])
async def sign_in(request):
    """
    登录接口
    :param request:
    :return:
    """

    params = request.json
    response_data = BaseResponse()
    try:
        account = params.get('account', '')
        password = params.get('password', '')

        if not all([account, password]):
            response_data.set_params_error()

        staff = Staff()
        staff_info = await staff.find_staff_by_mobile_or_nickname(mobile=account,nickname=account)
        if not staff_info:
            return response_data.set_no_exist_error()

        staff = staff.init_staff_info(**staff_info)

        if staff.check_staff_password(password):
            token = await create_access_token(app=request.app, identity='nickname',
                                              user_claims=json_util.dumps(staff_info))
            return response_data.set_response_success(data=token)
        else:
            return response_data.identity_authentication_error()

    except Exception as e:
        return response_data.set_system_error(message=e)


@blueprint.route(uri='/create/inner/info', methods=['POST'])
@response_exception
async def create_inner_info(request):
    """
    创建内部员工
    :param request:
    :return:
    """
    params = request.json
    response_data = BaseResponse()

    pass
