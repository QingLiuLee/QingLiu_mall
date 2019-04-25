# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
import asyncio
import pprint

from sanic import Blueprint
from sanic.response import json

from commodity.category.models import Category

blueprint = Blueprint(name="category", url_prefix="/category", version=1)


@blueprint.route(uri='/create/info', methods=['GET'])
async def create_category_info(request):
    test1 = await Category().get_info_list_by_pageSize()

    print(test1)
    return json({'result': 'success'})
