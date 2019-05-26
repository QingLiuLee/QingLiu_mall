# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:10 AM
# @Author   : Lee才晓
# @Describe :
from sanic_cors import CORS
from sanic_jinja2 import SanicJinja2
from sanic_jwt_extended import JWTManager

cors = CORS()
jinja2 = SanicJinja2()
jwt = JWTManager(app=None)
