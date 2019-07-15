# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:07 AM
# @Author   : Lee才晓
# @Describe :

from sanic import Sanic
from sanic_cors import CORS
from sanic_jwt_extended import JWTManager

import commodity
import consumer
import coupon
import integral
import merchant
import chat
from system import base_config
from system.extensions import socket_io
from system.response import *

app = Sanic()


def create_app():
    app.config.from_object(base_config)

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    JWTManager(app)
    CORS(app)

    socket_io.attach(app)
    return app


def register_blueprints(app):
    app.blueprint(commodity.blueprint_group)
    app.blueprint(merchant.blueprint_group)
    app.blueprint(consumer.blueprint_group)
    app.blueprint(coupon.blueprint_group)
    app.blueprint(integral.blueprint_group)
    app.blueprint(chat.blueprint_group)
    return app


@app.listener('before_server_start')
async def before_server_start(app, loop):
    pass


@app.listener('after_server_start')
async def after_server_start(app, loop):
    pass


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    pass


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    pass


@app.exception(NotFound)
def not_found(request, response):
    return response.response_json(message='请求地址错误', data=request.url)


@app.exception(ServerError)
def server_error(request, response):
    return response.response_json(message='服务器异常', data=response.message)


@app.exception(Unauthorized)
def unauthorized(request, response):
    return response.response_json(message='请求参数已过期', data='Authorization-token')


@app.exception(InvalidUsage)
def invalid_usage(request, response):
    return response.response_json(message='请求参数错误', data=response.message)


@app.exception(DataExistsError)
def data_exists_error(request, response):
    return response.response_json(message='数据重复错误', data=response.message)


@app.exception(NoExistsError)
def no_exists_error(request, response):
    return response.response_json(message='数据不存在', data=response.message)


@app.exception(JsonResponse)
def json_response(request, response):
    return response.response_json(message='请求成功', data=response.message)


@app.exception(HtmlResponse)
def html_response(request, response):
    return response.response_html()
