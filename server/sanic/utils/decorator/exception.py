# -*- coding: utf-8 -*-
# @Time     : 4/30/19 4:32 PM
# @Author   : Lee才晓
# @Describe :
from sanic.exceptions import abort
from sanic_jwt_extended import jwt_required

from system.response import ServerErrorCode


def try_except(func):
    def dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return dec


def response_exception(func):
    @jwt_required
    async def wrapper(request, *args, **kwargs):
        try:
            return await func(request, *args, **kwargs)
        except Exception as e:
            if hasattr(e, 'status_code'):
                raise e
            else:
                abort(status_code=ServerErrorCode, message=e)

    return wrapper
