# -*- coding: utf-8 -*-
# @Time     : 2019/7/10
# @Author   : Lee才晓
# @Describe :

from sanic import Blueprint

from . import views, chat_room

blueprint_group = Blueprint.group(views.blueprint, chat_room.views.blueprint, url_prefix='/chat')
