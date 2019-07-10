# -*- coding: utf-8 -*-
# @Time     : 4/24/19 1:15 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint

from . import category
from . import product

blueprint_group = Blueprint.group(category.views.blueprint, product.views.blueprint, url_prefix='/commodity')
