#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 10:11
# @Author  : Lee才晓
# @File    : response
# @Function:
from sanic.exceptions import abort, InvalidUsage, ServerError
from sanic.response import json

NormalCode = 200

ParamsErrorCode = 400  # 请求参数错误
UnAuthorizedCode = 401  # 身份认证过期
TimeOutCode = 408  # 连接超时

SystemErrorCode = 500  # 系统内部错误


class BaseResponse(object):
    """
    响应类
    """
    __slots__ = {
        'code', 'data', 'msg',
    }

    def __init__(self, code=SystemErrorCode, data=None, msg='系统异常', ):
        self.code = code
        self.data = data
        self.msg = msg

    def set_response_data(self, code=None, data=None, msg='', ):
        self.code = code
        self.data = data
        self.msg = msg

    def set_response_success(self, data='', msg='响应成功'):
        """
        响应成功
        :return:
        """
        return json(body={'code': NormalCode, 'msg': msg, 'data': data})

    def set_params_error(self, message='请求参数错误'):
        """
        请求参数错误
        :return:
        """
        abort(status_code=InvalidUsage.status_code, message=str(message))

    def set_system_error(self, message='系统内部错误'):
        """
        系统内部错误
        :return:
        """
        abort(status_code=ServerError.status_code, message=str(message))

    def set_exist_error(self, message='数据已存在'):
        """
        数据存在错误
        :return:
        """
        abort(status_code=InvalidUsage.status_code, message=str(message))

    def set_no_exist_error(self, message='数据不存在'):
        """
        数据不存在错误
        :return:
        """
        abort(status_code=InvalidUsage.status_code, message=str(message))

    def identity_authentication_error(self, message='身份认证错误'):
        """
        身份认证错误
        :return:
        """
        abort(status_code=InvalidUsage.status_code, message=str(message))

    def get_dict(self):
        data = {}
        for name in dir(self):
            if not name.startswith('__') and not hasattr(getattr(self, name), '__call__'):
                data[name] = getattr(self, name)

        return data
