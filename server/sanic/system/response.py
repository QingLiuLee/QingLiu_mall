#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 10:11
# @Author  : Lee才晓
# @File    : response
# @Function:
from sanic.exceptions import SanicException, add_status_code
from sanic.response import json, html

NormalCode = 200
JsonSuccessCode = 207
HtmlSuccessCode = 208

NotFoundCode = 404

ParamsErrorCode = 400  # 请求参数错误
UnAuthorizedCode = 401  # 身份认证过期
TimeOutCode = 408  # 连接超时

ServerErrorCode = 500  # 系统内部错误
ExistsErrorCode = 555  # 数据重复错误
NoExistsErrorCode = 556  # 数据不存在错误


class BaseResponse(SanicException):

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def response_json(self, message, data):
        return json(status=self.status_code, body={'msg': message, 'data': data})

    def response_html(self):
        with open(self.message) as f:
            return html(status=self.status_code, body=f.read())

    def get_dict(self):
        data = {}
        for name in dir(self):
            if not name.startswith('__') and not hasattr(getattr(self, name), '__call__'):
                data[name] = getattr(self, name)

        return data


@add_status_code(JsonSuccessCode)
class JsonResponse(BaseResponse):

    def __init__(self, message, status_code):
        super(JsonResponse, self).__init__(message=message, status_code=status_code)


@add_status_code(HtmlSuccessCode)
class HtmlResponse(BaseResponse):
    def __init__(self, message, status_code):
        super(HtmlResponse, self).__init__(message=message, status_code=status_code)


@add_status_code(NotFoundCode)
class NotFound(BaseResponse):

    def __init__(self, message, status_code):
        super(NotFound, self).__init__(message=message, status_code=status_code)


@add_status_code(ServerErrorCode)
class ServerError(BaseResponse):
    def __init__(self, message, status_code):
        super(ServerError, self).__init__(message=message, status_code=status_code)


@add_status_code(UnAuthorizedCode)
class Unauthorized(BaseResponse):
    def __init__(self, message, status_code):
        super(Unauthorized, self).__init__(message=message, status_code=status_code)


@add_status_code(ParamsErrorCode)
class InvalidUsage(BaseResponse):
    def __init__(self, message, status_code):
        super(InvalidUsage, self).__init__(message=message, status_code=status_code)


@add_status_code(ExistsErrorCode)
class DataExistsError(BaseResponse):
    def __init__(self, message, status_code):
        super(DataExistsError, self).__init__(message=message, status_code=status_code)


@add_status_code(NoExistsErrorCode)
class NoExistsError(BaseResponse):
    def __init__(self, message, status_code):
        super(NoExistsError, self).__init__(message=message, status_code=status_code)
