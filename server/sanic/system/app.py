# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:07 AM
# @Author   : Lee才晓
# @Describe :
from sanic import Sanic

from commodity import product_blueprint_group
from system.database import MotorBase

app = Sanic()


def create_app():
    register_blueprints(app)
    return app


def register_extensions(app):
    return app


def register_blueprints(app):
    app.blueprint(product_blueprint_group)
    return app


@app.listener('before_server_start')
async def setup_db(app, loop):
    pass
