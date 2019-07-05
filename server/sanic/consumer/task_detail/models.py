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
        'action_code',  # login_detail/order_detail
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
    def init_task_detail_info(cls, **kwargs):
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

    @try_except
    def get_task_detail_by_consumer_code_and_action_code_and_task_code(self):
        return self.find_one(condition={'$and': [{'consumer_code': self.consumer_code},
                                                 {'action_code': self.action_code},
                                                 {'task_code': self.task_code}]})

    @try_except
    def get_task_detail_by_code(self):
        return self.find_one(condition={'detail_code': self.detail_code})

    @try_except
    def set_task_detail_finish_status(self, is_finished=False):
        return self.update_one_by_custom(condition={'detail_code': self.detail_code},
                                         update={'$set': {'is_finished': is_finished}})

    @try_except
    def set_task_detail_reward_status(self, is_reward=False):
        return self.update_one_by_custom(condition={'detail_code': self.detail_code},
                                         update={'$set': {'is_reward': is_reward}})

    @try_except
    def get_task_detail_and_task_info(self):
        return self.aggregate_by_pipeline(pipeline=[
            {'$match': {'detail_code': self.detail_code}},
            {'$lookup': {
                'from': 'tasks',
                'localField': 'task_code',
                'foreignField': 'task_code',
                'as': 'tasks'
            }},
            {'$lookup': {
                'from': self.action_code,
                'localField': 'action_code',
                'foreignField': 'detail_code',
                'as': 'action_detail'
            }},
            {'$project': {
                '_id': {"$toString": "$_id"},
                'detail_code': 1,
                'consumer_code': 1,
                'action_code': 1,
                'is_finished': 1,
                'is_reward': 1,
                'task_info': '$tasks',
                'action_detail': '$action_detail',
            }}
        ])
