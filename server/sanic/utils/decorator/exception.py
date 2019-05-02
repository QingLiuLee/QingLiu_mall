# -*- coding: utf-8 -*-
# @Time     : 4/30/19 4:32 PM
# @Author   : Lee才晓
# @Describe :

from sanic.response import json


def try_except(func):
    def dec():
        try:
            func()
        except Exception as e:
            raise e

    return dec


def response_exception(func):
    def wrapper(request, *args, **kwargs):
        try:
            func(request, *args, **kwargs)
        except Exception as e:
            return json({'dec': '{0} 函数出现异常 {1}'.format(func.__name__, str(e))}), 500

    return wrapper
