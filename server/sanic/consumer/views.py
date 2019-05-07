# -*- coding: utf-8 -*-
# @Time     : 5/6/19 7:02 PM
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint

from consumer.models import Consumer, ConsumerBaseInfo
from system.response import BaseResponse

blueprint = Blueprint(name="consumer", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
async def create_admin_info(request):
    params = request.json
    response_data = BaseResponse()
    try:

        base_info = ConsumerBaseInfo.init_base_info(**params)

        if not base_info.check_params_is_none():
            return response_data.set_params_error()

        consumer = Consumer.init_consumer_info(base_info=base_info.get_json_by_obj())
        old_info = await consumer.find_consumer_by_mobile_or_nickname()
        if old_info:
            return response_data.set_exist_error()

        consumer_code = consumer.create_consumer_info()

        if consumer_code:
            return response_data.set_response_success()
        else:
            return response_data.set_system_error()
    except Exception as e:
        return response_data.set_system_error(message=e)
