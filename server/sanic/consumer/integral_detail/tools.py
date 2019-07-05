# -*- coding: utf-8 -*-
# @Time     : 2019/7/5
# @Author   : Lee才晓
# @Describe :
from consumer.integral_detail.models import IntegralDetail, IntegralHistoryInfo


def update_consumer_integral_detail(consumer_code, income_type, integral_value, detail):
    integral_detail = IntegralDetail.init_integral_detail(consumer_code=consumer_code)
    history_info = IntegralHistoryInfo.init_history_info(income_type=income_type,
                                                         integral_value=integral_value,
                                                         detail=detail)

    if not all([integral_detail.consumer_code, history_info.check_params_is_none(['create_time'])]):
        return False

    detail_info = await integral_detail.get_integral_detail_by_consumer_code()
    if not detail_info:
        return False

    if history_info.income_type > 0:
        integral_value = 1 * float(history_info.integral_value)
    elif history_info.income_type < 0:
        integral_value = -1 * float(history_info.integral_value)
    else:
        integral_value = 0

    result = await integral_detail.update_consumer_integral_detail(integral_value=integral_value,
                                                                   history_info=history_info)

    if result.modified_count:
        return True
    return False
