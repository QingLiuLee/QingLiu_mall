# -*- coding: utf-8 -*-
# @Time     : 4/30/19 6:13 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.response import json

from merchant.organization.models import Organization
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="organization", url_prefix="/organization", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_category_info(request):
    """
    创建商家信息接口
    :param request:
    :return:
    """
    params = request.json

    merchant_name = params.get('merchant_name', '')
    explain = params.get('explain', '')
    img_list = params.get('img_list', [])
    sale_type = params.get('sale_type', [])
    owner_code = params.get('owner_code', '')

    org_obj = Organization.init_org_info(params)
    org_code = await org_obj.create_org_info()

    if org_code:
        return json({'result': 'success'})
    else:
        return json({'result': 'failed'})
