# -*- coding: utf-8 -*-
# @Time     : 4/24/19 10:10 AM
# @Author   : Lee才晓
# @Describe :
from utils.authenticator import TokenAuth

auth = TokenAuth(secret_key='super-secret', header='Authentication-Token')
