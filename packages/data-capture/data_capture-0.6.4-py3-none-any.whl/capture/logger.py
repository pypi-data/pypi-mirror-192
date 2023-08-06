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
from .handler import HourTimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
from loguru import logger as loguru_logger

CAPTURE_LOG_TEMPLATE = 'request_id:{} request:{} response:{}'

CAPTURE_DATA_DIR = 'CAPTURE_DATA_DIR'
ENABLE_CAPTURE_REQUEST = 'ENABLE_CAPTURE_REQUEST'
ENABLE_CAPTURE_RESPONSE = 'ENABLE_CAPTURE_RESPONSE'





def cap(request_id: str, request=None, response=None):
    """
    text logger main func
    :param request_id:
    :param request:
    :param response:
    :return:
    """
    logger.info(CAPTURE_LOG_TEMPLATE.format(request_id, request, response))


def check_data_capture_disabled():
    """
    check if disable data capture, stop print log
    :return:
    """
    is_enable_request = os.environ.get(ENABLE_CAPTURE_REQUEST)
    is_enable_response = os.environ.get(ENABLE_CAPTURE_RESPONSE)
    return is_enable_request in ['False', None, ''] and \
        is_enable_response in ['False', None, '']


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    custom json formatter
    """
    def add_fields(self, log_record, record, message_dict):
        """
        add fields to log record for format
        :param log_record:
        :param record:
        :param message_dict:
        :return:
        """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['request_id'] = log_record['request'] = log_record['response'] = ''
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
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


def init(path) -> loguru_logger:
    """
    init capture logger
    :param path: log file dir
    :return: loguru logger
    """
    loguru_logger.remove(handler_id=None)
    handler = HourTimedRotatingFileHandler(path)
    formatter = CustomJsonFormatter('%(timestamp)s %(request_id)s %(request)s %(response)s')
    handler.setFormatter(formatter)
    loguru_logger.add(handler, enqueue=True)
    logger = loguru_logger.opt(lazy=True).opt(colors=False).opt(raw=True)
    if check_data_capture_disabled():
        logger.remove(handler_id=None)
    return logger


if os.environ.get(CAPTURE_DATA_DIR) is None:
    os.environ[CAPTURE_DATA_DIR] = '/home/model_data_capture/predictions/result.jsonl'

logger = init(os.environ[CAPTURE_DATA_DIR])
