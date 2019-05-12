# -*- coding: utf-8 -*-
# @Time     : 4/26/19 9:46 AM
# @Author   : Lee才晓
# @Describe : 

import codecs
import logging
from logging import *

# 指定日志的格式，按照每天一个日志文件的方式
import os

import time


class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode, encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        自定义日志切分，因logging与多进程的原因
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_base_filename(record):
                self.build_base_filename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_base_filename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.baseFilename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_base_filename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()


LogPath = os.getcwd() + '/logs/{0}.log'.format('mall')

LogConfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(filename)s] [line:%(lineno)d] : %(message)s'
        },
        'verbose': {
            'format':
                '[%(asctime)s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] : %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # TODO
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',  # TODO
            'class': 'system.log_config.SafeFileHandler',
            'formatter': 'verbose',
            'filename': LogPath,
            # 'when': 'D',
            # 'interval': 1,
            'encoding': 'utf8',
            'mode': 'a'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

logger = logging.getLogger('root')
