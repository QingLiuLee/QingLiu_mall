# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:17 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_jwt_extended import create_access_token, jwt_required
from sanic_jwt_extended.tokens import Token

from commodity.category.models import Category

blueprint = Blueprint(name="category", url_prefix="/category", version=1)


@blueprint.route(uri='/create/info', methods=['GET'])
async def create_category_info(request):
    params = request.json

    category = Category(**{'category_name': 'test'})
    await category.create_info()

    return json({'result': 'success'})


@blueprint.route(uri='/test', methods=['GET', 'POST'])
async def test(request):
    user_claim = {"VERI TAS": "LUX MEA"}
    token = await create_access_token(app=request.app, identity='username', user_claims=user_claim)
    print(token)
    return json({'token': token})


@blueprint.route('/protected', methods=['GET', 'POST'])
@jwt_required
async def protected(request: Request, token: Token):
    print('access token')
