# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:07 AM
# @Author   : Lee才晓
# @Describe :
from sanic import Sanic
from sanic.exceptions import NotFound, ServerError, Unauthorized, InvalidUsage
from sanic.response import json
from sanic_cors import CORS
from sanic_jwt_extended import JWTManager

import commodity
import merchant
from system import base_config

app = Sanic()


def create_app():
    app.config.from_object(base_config)

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    JWTManager(app)
    CORS(app)
    return app


def register_blueprints(app):
    app.blueprint(commodity.product_blueprint_group)
    app.blueprint(merchant.product_blueprint_group)
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
async def not_found(request, exception):
    return json(body={'code': NotFound.status_code, 'msg': '{0} 请求函数找不到'.format(str(request))},
                status=NotFound.status_code)


@app.exception(ServerError)
async def server_error(request, exception):
    return json(body={'code': ServerError.status_code, 'msg': '{0} 请求函数出现异常 {1}'.format(str(request), str(exception))},
                status=ServerError.status_code)


@app.exception(Unauthorized)
async def unauthorized(request, exception):
    return json(body={'code': Unauthorized.status_code, 'msg': '{0} 请求函数token 已过期'.format(str(request))},
                status=Unauthorized.status_code)


@app.exception(InvalidUsage)
async def invalid_usage(request, exception):
    return json(body={'code': InvalidUsage.status_code, 'msg': '{0} 请求函数出现错误 {1}'.format(str(request), str(exception))},
                status=InvalidUsage.status_code)
