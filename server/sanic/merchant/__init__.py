# -*- coding: utf-8 -*-
# @Time     : 4/30/19 4:21 PM
# @Author   : Lee才晓
# @Describe : 商家模块
from sanic import Blueprint

from . import organization, staff

blueprint_group = Blueprint.group(organization.views.blueprint, staff.views.blueprint, url_prefix='/merchant')
