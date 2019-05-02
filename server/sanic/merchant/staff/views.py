# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:12 PM
# @Author   : Lee才晓
# @Describe : 
from sanic import Blueprint
from sanic.response import json

from merchant.staff.models import Staff
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="staff", url_prefix="/staff", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_staff_info(request):
    params = request.json

    mobile = params.get('mobile')
    nickname = params.get('nickname')
    password = params.get('password')

    staff = Staff.init_staff_info(**params)
    staff_code = staff.create_staff_info()

    if staff_code:
        return json({'result': 'success'})
    else:
        return json({'result': 'failed'})
