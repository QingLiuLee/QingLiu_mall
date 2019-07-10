# -*- coding: utf-8 -*-
# @Time     : 6/17/19 7:23 PM
# @Author   : Lee才晓
# @Describe : 
from sanic import Blueprint

from . import views

blueprint_group = Blueprint.group(views.blueprint, url_prefix='/coupon')
