# -*- coding: utf-8 -*-
# @Time     : 4/24/19 8:11 PM
# @Author   : Lee才晓
# @Describe : 

from sanic import Blueprint
from sanic.response import json

blueprint = Blueprint(name="product", url_prefix="/product", version=1)


@blueprint.route(uri='/create/info', methods=['GET'])
async def create_product_info(request):
    return json({'result': 'success'})
