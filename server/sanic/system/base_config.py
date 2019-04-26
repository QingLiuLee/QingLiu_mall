# -*- coding: utf-8 -*-
# @Time     : 4/24/19 7:56 PM
# @Author   : Lee才晓
# @Describe :
from system import log_config

MONGODB = dict(
    MONGO_HOST='107.172.122.19',
    MONGO_PORT='27017',
    MONGO_USERNAME='lee',
    MONGO_PASSWORD='10241026',
    DATABASE='qingliu_mall',
)

# 日志配置
LOGCONFIG = log_config.LogConfig
LOGCONFIG_QUEUE = ['root']