# -*- coding: utf-8 -*-
# @Time     : 2019/7/10
# @Author   : Lee才晓
# @Describe :

from sanic import Blueprint

from . import views

blueprint_group = Blueprint.group(views.blueprint, url_prefix='/chat')
