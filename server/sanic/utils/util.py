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