# -*- coding: utf-8 -*-
# @Time     : 2019/7/8
# @Author   : Lee才晓
# @Describe :
from system.base_model import IBaseModel


class Audit(IBaseModel):
    __slots__ = {
        'audit_code',
        'type',
        'create_time',
        'vail_status',
        'reason',
        'org_code',
    }

    def __init__(self, **kwargs):
        super(Audit, self).__init__('audit')
        self.audit_code = kwargs.get('audit_code', '')
        self.type = kwargs.get('type', 0)
        self.create_time = kwargs.get('create_time', None)
        self.vail_status = kwargs.get('vail_status', False)
        self.reason = kwargs.get('reason', '')
