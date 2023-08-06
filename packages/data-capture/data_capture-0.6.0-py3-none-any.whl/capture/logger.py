# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
capture logger library
"""
import os
import re
import time
from datetime import datetime
from logging import handlers
from pythonjsonlogger import jsonlogger
from loguru import logger as loguru_logger

TIME_DIRECTORY_FORMAT = '%Y-%m-%d/%H'
CAPTURE_LOG_TEMPLATE = 'request_id:{} request:{} response:{}'
ENABLE_CAPTURE_REQUEST = 'ENABLE_CAPTURE_REQUEST'
ENABLE_CAPTURE_RESPONSE = 'ENABLE_CAPTURE_RESPONSE'


class HourTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to files rotated into time directories, rotating every hour
    examples:
    1. filename = result.log        => logging into yyyy-mm-dd/hh/result.log
    2. filename = xxx/result.log    => logging into xxx/yyyy-mm-dd/hh/result.log
    3. filename = /xxx/result.log   => logging into /xxx/yyyy-mm-dd/hh/result.log

    disable backupCount feature for the moment, since delete files among many directories is complex and ineffective
    """

    def __init__(self, filename, encoding=None, delay=False, utc=False, atTime=None):
        # record baseDir
        self.baseDir = os.path.dirname(os.path.abspath(filename))
        # generate time directory
        timeTuple = time.localtime(int(time.time()))
        dirName = os.path.join(self.baseDir, time.strftime(TIME_DIRECTORY_FORMAT, timeTuple))
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        # merge time directory into filename
        filename = os.path.join(dirName, os.path.basename(filename))
        handlers.TimedRotatingFileHandler.__init__(self, filename, 'H', 1, 0, encoding, delay, utc, atTime)

    def shouldRollover(self, record) -> int:
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:
            self.stream = self._open()
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)

        dirName = os.path.join(self.baseDir, time.strftime(TIME_DIRECTORY_FORMAT, timeTuple))
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        dfn = os.path.join(dirName, os.path.basename(self.baseFilename))

        if os.path.exists(dfn):
            os.remove(dfn)

        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def exitRollover(self):
        self.delay = True
        if self.stream:
            if self.stream.tell() > 0:
                self.doRollover()


def cap(request_id: str, request=None, response=None):
    logger.info(CAPTURE_LOG_TEMPLATE.format(request_id, request, response))


def check_data_capture_disabled():
    is_enable_request = os.environ.get(ENABLE_CAPTURE_REQUEST)
    is_enable_response = os.environ.get(ENABLE_CAPTURE_RESPONSE)
    return is_enable_request in ['False', ''] and is_enable_response in ['False', '']


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['request_id'] = log_record['request'] = log_record['response'] = ''
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if isinstance(record.msg, str):
            request_id = re.findall(r"request_id:(.+?) request", record.msg)
            if len(request_id) > 0:
                log_record['request_id'] = request_id[0]
            request = re.findall(r"request:(.+?) response", record.msg)
            if len(request) > 0 and os.environ.get(ENABLE_CAPTURE_REQUEST) == "True":
                log_record['request'] = request[0]
            response = re.findall(r"response:(.+)", record.msg)
            if len(response) > 0 and os.environ.get(ENABLE_CAPTURE_RESPONSE) == "True":
                log_record['response'] = response[0]

def init(path, logger) -> loguru_logger:
    """"""
    logger.remove()
    handler = HourTimedRotatingFileHandler(path)
    formatter = CustomJsonFormatter('%(timestamp)s %(request_id)s %(request)s %(response)s')
    handler.setFormatter(formatter)
    logger.add(handler, enqueue=True)
    logger = logger.opt(lazy=True).opt(colors=False).opt(raw=True)
    if check_data_capture_disabled():
        logger.remove()



if os.environ.get('CAPTURE_DATA_DIR') is None:
    os.environ['CAPTURE_DATA_DIR'] = '/home/model_data_capture/result.jsonl'

logger = init(os.environ['CAPTURE_DATA_DIR'], loguru_logger)
