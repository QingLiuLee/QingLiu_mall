# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.response import json

from commodity.category.models import Category

blueprint = Blueprint(name="category", url_prefix="/category", version=1)


@blueprint.route(uri='/create/info', methods=['GET'])
async def create_category_info(request):

    params = request.json

    # create_info_result = await Category().create_info()

    category = Category()
    category.init_data(**{'category_name':'test'})
    await category.create_model_info()

    return json({'result': 'success'})
