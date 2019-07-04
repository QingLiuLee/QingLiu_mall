# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class TasksDetail(IBaseModel):
    __slots__ = {
        'detail_code',
        'consumer_code',
        'action_code',
        'create_time',
        'task_code',
        'is_finished',  # True/False
        'is_reward',  # True/False
    }

    def __init__(self, **kwargs):
        super(TasksDetail, self).__init__('task_detail')
        self.detail_code = kwargs.get('detail_code', '')
        self.consumer_code = kwargs.get('consumer_code', '')
        self.action_code = kwargs.get('action_code', '')
        self.create_time = kwargs.get('create_time', None)
        self.task_code = kwargs.get('task_code')
        self.is_finished = kwargs.get('is_finished', False)
        self.is_reward = kwargs.get('is_reward', False)

    @classmethod
    @try_except
    def init_task_info(cls, **kwargs):
        task_detail = cls()
        task_detail.detail_code = kwargs.get('detail_code', '')
        task_detail.consumer_code = kwargs.get('consumer_code', '')
        task_detail.action_code = kwargs.get('action_code', '')
        task_detail.create_time = kwargs.get('create_time', None)
        task_detail.task_code = kwargs.get('task_code')
        task_detail.is_finished = kwargs.get('is_finished', False)
        task_detail.is_reward = kwargs.get('is_reward', False)
        return task_detail

    @try_except
    def create_task_detail_info(self):
        self.create_time = datetime.datetime.now()
        self.detail_code = make_code_or_id('task_detail_')
        self.create_info()
        return self.detail_code
