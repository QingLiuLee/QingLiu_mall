# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:07 AM
# @Author   : Lee才晓
# @Describe :
from sanic import Sanic

from commodity import product_blueprint_group
from system import base_config

app = Sanic()


def create_app():
    app.config.from_object(base_config)

    register_blueprints(app)
    return app


def register_extensions(app):
    return app


def register_blueprints(app):
    app.blueprint(product_blueprint_group)
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
