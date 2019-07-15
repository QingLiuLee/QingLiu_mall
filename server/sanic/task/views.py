# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic_jwt_extended.tokens import Token

from system.response import ParamsErrorCode, ExistsErrorCode, JsonSuccessCode, ServerErrorCode, NoExistsErrorCode
from task.models import Tasks
from utils.decorator.exception import response_exception

blueprint = Blueprint(name="tasks", version=1)


@blueprint.route(uri='/create/info', methods=['POST'])
@response_exception
async def create_task_info(request: Request, token: Token):
    """
    :name create_task_info
    :param (explain/start_time/end_time/available_type/reward_type/reward_code/reward_num/is_daily_tasks)
    """

    params = request.json

    task = Tasks.init_task_info(**params)

    if not all(task.check_params_is_none(['task_code', 'create_time'])):
        abort(status_code=ParamsErrorCode)

    is_exists = await task.get_task_by_explain()
    if is_exists:
        abort(status_code=ExistsErrorCode, message='the task already exists.')

    task_code = task.create_task_info()
    if task_code:
        abort(status_code=JsonSuccessCode, message={'task_code': task_code})

    abort(status_code=ServerErrorCode, message='create the task failed.')


@blueprint.route(uri='/update/info', methods=['POST'])
@response_exception
async def update_task_info(request: Request, token: Token):
    """
    :name update_task_info
    :param (task_code/explain/start_time/end_time/available_type/reward_type/reward_code/reward_num)
    """

    params = request.json

    task = Tasks.init_task_info(**params)

    if not all(task.check_params_is_none(['create_time'])):
        abort(status_code=ParamsErrorCode)

    task_info = await task.get_task_by_explain()
    if not task_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    result = task.update_task_info()
    if result.modified_count or result.matched_count:
        abort(status_code=JsonSuccessCode, message='update the task success')

    abort(status_code=ServerErrorCode, message='update the task failed.')


@blueprint.route(uri='/delete/task/info', methods=['POST'])
@response_exception
async def delete_task_info(request: Request, token: Token):
    """
    :name delete_task_info
    :param (task_code)
    """

    params = request.json

    task = Tasks.init_task_info(**params)

    if not task.task_code:
        abort(status_code=ParamsErrorCode)

    task_info = await task.get_task_by_explain()
    if not task_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    result = task.delete_task_info()
    if result.raw_result and result.raw_result.ok:
        abort(status_code=JsonSuccessCode, message='delete the task success')

    abort(status_code=ServerErrorCode, message='delete the task failed.')


@blueprint.route(uri='/get/info', methods=['POST'])
@response_exception
async def get_task_info(request: Request, token: Token):
    """
    :name  get_task_info_by_code
    :param (task_code)
    """

    params = request.json
    task = Tasks.init_task_info(**params)

    if not task.task_code:
        abort(status_code=ParamsErrorCode)

    task_info = await task.get_task_by_code()
    if not task_info:
        abort(status_code=NoExistsErrorCode, message='the task no exists.')

    abort(status_code=JsonSuccessCode, message={'task_info': task_info})


@blueprint.route(uri='/get/daily/task', methods=['POST'])
@response_exception
async def get_daily_task(request: Request, token: Token):
    """
    :name get_daily_task
    :param ()
    """
    params = request.json
    task = Tasks.init_task_info(**params)

    task_list = await task.get_daily_tasks()
    abort(status_code=JsonSuccessCode, message={'daily_task': task_list})
