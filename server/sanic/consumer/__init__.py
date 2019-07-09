# -*- coding: utf-8 -*-
# @Time     : 4/30/19 5:23 PM
# @Author   : Lee才晓
# @Describe : 消费者信息
from sanic import Blueprint
from . import base_info, integral_detail, login_detail

product_blueprint_group = Blueprint.group(base_info.views.blueprint, login_detail.views.blueprint,
                                          integral_detail.views.blueprint,
                                          url_prefix='/consumer')
