# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
capture logger library
"""
import json
import os
from datetime import datetime
from loguru import logger as loguru_logger
from .handler import HourTimedRotatingFileHandler

CAPTURE_DATA_DIR = 'CAPTURE_DATA_DIR'
DEFAULT_CAPTURE_FILE_PATH = 'home/model_data_capture/predictions/result.jsonl'
CAPTURE_REQUEST = 'CAPTURE_REQUEST'
CAPTURE_RESPONSE = 'CAPTURE_RESPONSE'


class CaptureLogger:
    def __init__(self, log_dir_path: str):
        """
        init logger
        :param log_dir_path:
        """
        self.log_dir_path = log_dir_path
        self.is_enable_capture_request = os.environ.get(CAPTURE_REQUEST)
        self.is_enable_capture_response = os.environ.get(CAPTURE_RESPONSE)
        # 取消console log的输出
        loguru_logger.remove(handler_id=None)
        loguru_logger.add(HourTimedRotatingFileHandler(self.log_dir_path), enqueue=True)
        self._logger = loguru_logger.opt(lazy=True).opt(colors=False).opt(raw=True)
        if self.check_data_capture_disabled():
            self._logger.remove(handler_id=None)

    def check_data_capture_disabled(self):
        """
        check if need print log
        :return:
        """
        return self.is_enable_capture_request != 'enable' and \
            self.is_enable_capture_response != 'enable'

    def cap(self, request_id: str, request=None, response=None):
        """
        cap log main func
        :param request_id:
        :param request:
        :param response:
        :return:
        """
        if isinstance(request, str) is False:
            request = json.dumps(request)
        if isinstance(response, str) is False:
            response = json.dumps(response)
        message = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "request_id": request_id,
            "request": request,
            "response": response,
        }
        json_encode_message = json.dumps(message)
        self._logger.info(json_encode_message)


if os.environ.get(CAPTURE_DATA_DIR) is None:
    os.environ[CAPTURE_DATA_DIR] = DEFAULT_CAPTURE_FILE_PATH

logger = CaptureLogger(os.environ[CAPTURE_DATA_DIR])
