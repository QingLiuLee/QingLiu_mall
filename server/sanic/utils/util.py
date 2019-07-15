# -*- coding: utf-8 -*-
# @Time     : 4/26/19 10:50 AM
# @Author   : Lee才晓
# @Describe : 

# 编码生成器
import datetime
import random


def make_code_or_id(prefix):
    """
    :param prefix: 首字母
    :return:
    """

    return prefix + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 100))


def get_current_zero_and_last_time():
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取今天零点
    zero_time = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
    # 获取23:59:59
    last_time = zero_time + datetime.timedelta(hours=23, minutes=59, seconds=59)

    return zero_time, last_time
