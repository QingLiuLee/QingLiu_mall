# -*- coding: utf-8 -*-
# @Time     : 4/24/19 7:55 PM
# @Author   : Lee才晓
# @Describe :
from functools import wraps


def singleton(cls):
    """
    用装饰器实现的实例 不明白装饰器可见附录 装饰器：https://github.com/howie6879/Sanic-For-Pythoneer/blob/master/docs/part2/%E9%99%84%E5%BD%95%EF%BC%9A%E5%85%B3%E4%BA%8E%E8%A3%85%E9%A5%B0%E5%99%A8.md
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance