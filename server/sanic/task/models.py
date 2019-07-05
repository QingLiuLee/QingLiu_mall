# -*- coding: utf-8 -*-
# @Time     : 2019/7/4
# @Author   : Lee才晓
# @Describe :
import datetime

from system.base_model import IBaseModel
from utils.constant import *
from utils.decorator.exception import try_except
from utils.util import make_code_or_id


class Tasks(IBaseModel):
    __slots__ = {
        'task_code',
        'explain',
        'create_time',
        'start_time',
        'end_time',
        'available_type',  # 1: no limit  2:vip  3:ordinary users
        'reward_type',  # 1:integral  2:coupon 3:cash 4:product
        'reward_code',
        'reward_num',
    }

    def __init__(self, **kwargs):
        super(Tasks, self).__init__('tasks')
        self.task_code = kwargs.get('task_code', '')
        self.explain = kwargs.get('explain', '')
        self.create_time = kwargs.get('create_time', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.available_type = kwargs.get('available_type', 0)
        self.reward_type = kwargs.get('reward_type', 0)
        self.reward_code = kwargs.get('reward_code', '')
        self.reward_num = kwargs.get('reward_num', 0)

    @classmethod
    @try_except
    def init_task_info(cls, **kwargs):
        task = cls()
        task.task_code = kwargs.get('task_code', '')
        task.explain = kwargs.get('explain', '')
        task.create_time = kwargs.get('create_time', None)
        task.start_time = kwargs.get('start_time', None)
        task.end_time = kwargs.get('end_time', None)
        task.available_type = kwargs.get('available_type', 0)
        task.reward_type = kwargs.get('reward_type', 0)
        task.reward_code = kwargs.get('reward_code', '')
        task.reward_num = kwargs.get('reward_num', 0)
        return task

    @try_except
    def create_task_info(self):
        self.task_code = make_code_or_id('tasks_')
        self.create_time = datetime.datetime.now()
        self.create_info()
        return self.task_code

    @try_except
    def get_task_by_explain(self):
        return self.find_one(condition={'explain': self.explain})

    @try_except
    def get_task_by_code(self):
        return self.find_one(condition={'task_code': self.task_code})

    @try_except
    def get_reward_info_by_reward_type(self):
        pipeline = [{'$match': {'task_code': self.task_code}}]
        if self.reward_type == INTEGRAL_TYPE:
            pipeline.append(
                {'$lookup': {
                    'from': INTEGRAL_TYPE,
                    'localField': 'reward_code',
                    'foreignField': 'integral_code',
                    'as': 'reward_info'
                }})
        elif self.reward_code == COUPON_TYPE:
            pipeline.append(
                {'$lookup': {
                    'from': COUPON_TYPE,
                    'localField': 'reward_code',
                    'foreignField': 'coupon_code',
                    'as': 'reward_info'
                }})

        return self.aggregate_by_pipeline(pipeline=[

            {'$project': {
                '_id': {"$toString": "$_id"},
                'task_code': 1,
                'explain': 1,
                'create_time': 1,
                'start_time': 1,
                'end_time': 1,
                'available_type': 1,  # 1: no limit  2:vip  3:ordinary users
                'reward_type': 1,  # 1:integral  2:coupon 3:cash 4:product
                'reward_num': 1,
                'reward_info': '$reward_info',
            }}
        ])
