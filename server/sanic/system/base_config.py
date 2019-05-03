# -*- coding: utf-8 -*-
# @Time     : 4/24/19 7:56 PM
# @Author   : Lee才晓
# @Describe :
from system import log_config

MONGODB = dict(
    MONGO_HOST='127.0.0.1',
    MONGO_PORT='27017',
    MONGO_USERNAME='lee',
    MONGO_PASSWORD='10241026',
    DATABASE='qingliu_mall',
)

# 日志配置
LOGCONFIG = log_config.LogConfig
LOGCONFIG_QUEUE = ['root']

JWT_SECRET_KEY = 'super-secret'
JWT_TOKEN_LOCATION = 'headers'
JWT_ALGORITHM = 'HS256'
JWT_IDENTITY_CLAIM = 'identity'
JWT_USER_CLAIMS = 'user_claims'
JWT_HEADER_NAME = 'Authorization-token'
JWT_HEADER_TYPE = ''
