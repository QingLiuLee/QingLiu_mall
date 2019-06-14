# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe :
from bson import json_util
from sanic import Blueprint
from sanic.request import Request
from sanic_jwt_extended import create_access_token
from sanic_jwt_extended.tokens import Token

from merchant.staff.models import Staff
from system.response import *
from utils.decorator.exception import *

blueprint = Blueprint(name="staff", url_prefix="/staff", version=1)


@blueprint.route(uri='/create/administrators/info', methods=['POST'])
async def create_admin_info(request):
    params = request.json
    mobile = params.get('mobile', '')
    nickname = params.get('nickname', '')
    password = params.get('password', '')

    if not all([mobile, nickname, password]):
        abort(status_code=ParamsErrorCode)

    staff = Staff()
    staff_info = await staff.find_staff_by_mobile_or_nickname(mobile=mobile, nickname=nickname)
    if staff_info:
        abort(status_code=ExistsErrorCode, message='手机号或昵称已存在')

    staff = staff.init_staff_info(mobile=mobile, nickname=nickname, password=password)
    staff_code = staff.create_admin_info()

    if staff_code:
        abort(status_code=JsonSuccessCode, message=staff_code)
    else:
        abort(status_code=ServerErrorCode, message='账号创建失败')


@blueprint.route(uri='/sign/in', methods=['POST'])
async def sign_in(request):
    """
    登录接口
    :param request:
    :return:
    """

    params = request.json
    account = params.get('account', '')
    password = params.get('password', '')

    if not all([account, password]):
        abort(status_code=ParamsErrorCode)

    staff = Staff()
    staff_info = await staff.find_staff_by_mobile_or_nickname(mobile=account, nickname=account)
    if not staff_info:
        abort(status_code=NoExistsErrorCode, message='当前账号不存在')

    staff = staff.init_staff_info(**staff_info)

    if staff.check_staff_password(password):
        token = await create_access_token(app=request.app, identity='nickname',
                                          user_claims=json_util.dumps(staff_info))
        abort(status_code=JsonSuccessCode, message={'token': token, 'staff_code': staff.staff_code})
    else:
        abort(status_code=UnAuthorizedCode, message='账号或密码错误')


@blueprint.route(uri='/create/inner/info', methods=['POST'])
@response_exception
async def create_inner_info(request: Request, token: Token):
    """
    创建内部员工
    :param request:
    :return:
    """
    params = request.json

    mobile = params.get('mobile', '')
    nickname = params.get('nickname', '')
    password = params.get('password', '')
    role_name = params.get('role_name', '')
    org_code = params.get('org_code', '')

    if not all([mobile, nickname, password, role_name, org_code]):
        abort(status_code=ParamsErrorCode)

    staff = Staff.init_staff_info(**params)
    staff_info = await staff.find_staff_by_mobile_or_nickname(mobile=mobile, nickname=nickname)
    if staff_info:
        abort(status_code=ExistsErrorCode, message='手机号或昵称已存在')

    staff_code = staff.create_admin_info()

    if staff_code:
        await staff.set_org_roles_by_staff_code(org_code=org_code, role_name=role_name)
        abort(status_code=JsonSuccessCode, message=staff_code)

    abort(status_code=ServerErrorCode, message='创建账号失败')


@blueprint.route(uri='/get/inner/list', methods=['POST'])
@response_exception
async def get_inner_list(request: Request, token: Token):
    """
    获取内部员工列表
    :param request:
    :param token:
    :return:
    """
    params = request.json

    org_code = params.get('org_code', '')
    if not all([org_code]):
        abort(status_code=ParamsErrorCode)

    staff = Staff()
    staff_list = await staff.get_staff_list_by_org_code(org_code=org_code)
    total_count = await staff.get_all_staff_count_by_org_code(org_code=org_code)

    for staff in staff_list:
        staff['_id'] = str(staff['_id'])
        staff['create_time'] = staff['create_time'].strftime('%Y-%m-%d %H:%M:%S')

    abort(status_code=JsonSuccessCode, message={"list": staff_list, "count": total_count})


@blueprint.route(uri='/unregister', methods=['POST'])
@response_exception
async def unregister_staff(request: Request, token: Token):
    """注销当前用户信息"""
    params = request.json

    staff_code = params.get('staff_code', '')
    if not staff_code:
        abort(status_code=ParamsErrorCode)

    staff = Staff.init_staff_info(**params)
    remove_result = await staff.remove_account()

    if remove_result.deleted_count:
        abort(status_code=JsonSuccessCode, message='账号已移除')
    else:
        abort(status_code=JsonSuccessCode, message='找不到该账号')


@blueprint.route(uri='/remove/inner/info', methods=['POST'])
@response_exception
async def remove_inner_staff(request: Request, token: Token):
    """移除内部员工"""

    params = request.json

    org_code = params.get('org_code', '')

    staff = Staff.init_staff_info(**params)

    if not all([org_code, staff.staff_code]):
        abort(status_code=ParamsErrorCode)

    staff_info = await staff.get_staff_info_by_staff_code()
    if not staff_info:
        abort(status_code=NoExistsErrorCode, message='当前账号不存在')

    role_result = staff.get_role_info_by_org_code(role_list=staff_info['roles'], org_code=org_code)
    if not role_result:
        abort(status_code=JsonSuccessCode, message='当前账号与机构无关联')

    await staff.set_role_end_time_by_org_code(org_code=org_code)
    abort(status_code=JsonSuccessCode, message='已移除该账号与机构的关联')


@blueprint.route(uri='/drop/collection', methods=['POST'])
@response_exception
async def drop_collection(request: Request, token: Token):
    """删除员工collection"""

    staff = Staff()
    await staff.drop_collection()
    abort(status_code=JsonSuccessCode, message='员工表已清除')

