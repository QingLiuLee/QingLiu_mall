# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from consumer.integral_detail.tools import update_consumer_integral_detail
from consumer.task_detail.models import TasksDetail
from system.response import *
from task.models import Tasks
from utils.constant import INTEGRAL_TYPE, COUPON_TYPE, INCOME_TYPE_ADD
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="task_detail", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_task_detail_info(request: Request, token: Token):
    """
    :name create_task_detail_info
    :param (consumer_code/action_code/task_code)
    """

    params = request.json

    task_detail = TasksDetail.init_task_detail_info(**params)

    if not all(task_detail.check_params_is_none(['detail_code', 'create_time', 'is_finished', 'is_reward'])):
        abort(status_code=ParamsErrorCode)

    is_exists = await task_detail.get_task_detail_by_consumer_code_and_action_code_and_task_code()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='the task already exists.')

    task_code = task_detail.create_task_detail_info()
    if task_code:
        abort(status_code=JsonSuccessCode, message={'task_code': task_code})

    abort(status_code=ServerErrorCode, message='create the task failed.')


@blueprint.route(uri='/get/info/by/code', methods=['POST'])
@response_exception
async def get_task_detail_info_by_code(request: Request, token: Token):
    """
    :name get_task_detail_info_by_code
    :param (detail_code)
    """
    params = request.json

    task_detail = TasksDetail.init_task_detail_info(**params)

    if not task_detail.detail_code:
        abort(status_code=ParamsErrorCode)

    task_detail_info = await task_detail.get_task_detail_and_task_info()
    if not task_detail_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    abort(status_code=JsonSuccessCode, message={'task_detail': task_detail_info})


@blueprint.route(uri='/finish/info', methods=["POST"])
@response_exception
async def finish_task_detail_info(request: Request, token: Token):
    """
    :name finish_task_detail_info
    :param (detail_code)
    """
    params = request.json

    task_detail = TasksDetail.init_task_detail_info(**params)

    if not task_detail.detail_code:
        abort(status_code=ParamsErrorCode)

    result = task_detail.set_task_detail_finish_status(is_finished=True)
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message={'result': result})
    abort(status_code=ServerErrorCode, message='the task_detail finish failed')


@blueprint.route(uri='/reward/info', methods=["POST"])
@response_exception
async def reward_task_detail_info(request: Request, token: Token):
    """
    :name reward_task_detail_info
    :param (detail_code)
    """
    params = request.json

    task_detail = TasksDetail.init_task_detail_info(**params)

    if not task_detail.detail_code:
        abort(status_code=ParamsErrorCode)

    task_detail_info = task_detail.get_task_detail_by_code()

    if task_detail_info['task_code']:
        reward_info = Tasks.init_task_info(task_code=task_detail_info['task_code']).get_reward_info_by_reward_type()

        if reward_info['reward_type'] == INTEGRAL_TYPE:
            result = update_consumer_integral_detail(consumer_code=task_detail.consumer_code,
                                                     income_type=INCOME_TYPE_ADD,
                                                     integral_value=reward_info['reward_info']['integral_value'],
                                                     detail=reward_info)
        elif reward_info['reward_type'] == COUPON_TYPE:
            result = None
        else:
            result = None

        if not result:
            abort(status_code=ServerErrorCode, message='the task_detail reward failed')

    result = task_detail.set_task_detail_reward_status(is_reward=True)
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message={'result': result})
    abort(status_code=ServerErrorCode, message='the task_detail reward failed')
