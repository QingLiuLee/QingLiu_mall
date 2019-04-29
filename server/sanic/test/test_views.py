#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 23:31
# @Author  : Lee才晓
# @File    : test_views
# @Function:
from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.get('/')
def app_test(request):
    return json({'result': '123'})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
