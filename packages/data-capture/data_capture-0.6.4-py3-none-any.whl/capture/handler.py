# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
import datetime
from logging import handlers
import os
import time

TIME_DIRECTORY_FORMAT = '%Y-%m-%d/%H'
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
                    addend = 1
                else:
                    addend = -1
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