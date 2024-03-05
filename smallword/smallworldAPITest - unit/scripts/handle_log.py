# -*- coding: utf-8 -*-
import time

import os
import logging
from logging.handlers import RotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler

from scripts.constants import LOGS_DIR
from scripts.handle_config import do_config


class HandleLog:
    """
    封装处理日志的类
    """
    def __init__(self):
        self.case_logger = logging.getLogger(do_config("log", "logger_name"))  # 如果不传name参数，那么默认使用root根收集器

        # 2、指定日志收集器的日志等级（装菜的容器对装菜种类的限制）
        self.case_logger.setLevel(do_config("log", "logger_level"))  # 往往会比较低

        # 3、定义日志输出渠道（装好的菜，放置的地方）
        # 输出到console控制台
        console_handle = logging.StreamHandler()

        # 输出到文件中
        # file_handle = RotatingFileHandler(filename=do_config("log", "log_filename"),
        #                                   maxBytes=do_config("log", "maxBytes"),
        #                                   backupCount=do_config("log", "backupCount"),
        #                                   encoding="utf-8")
        file_handle = ConcurrentRotatingFileHandler(filename=os.path.join(LOGS_DIR, do_config("log", "log_filename")),
                                                    maxBytes=do_config("log", "maxBytes"),
                                                    backupCount=do_config("log", "backupCount"),
                                                    encoding="utf-8")

        # 4、指定日志输出渠道的日志等级
        console_handle.setLevel(do_config("log", "console_level"))  # 如果都不能够被日志收集器收集的日志，一定没办法输出到渠道中
        file_handle.setLevel(do_config("log", "file_level"))

        # 5、定义日志显示的格式
        simple_formatter = logging.Formatter(do_config("log", "simple_formatter"))  # 简单的日志格式
        verbose_formatter = logging.Formatter(do_config("log", "verbose_formatter"))  # 复杂的日志格式

        console_handle.setFormatter(simple_formatter)  # 设置终端的日志为简单格式
        file_handle.setFormatter(verbose_formatter)  # 设置终端的日志为复杂格式

        # 6、对接，将日志器收集器与输出渠道进行对接，相当如将讲装菜的盘子放在马桶盖
        self.case_logger.addHandler(console_handle)
        self.case_logger.addHandler(file_handle)

    def get_logger(self):
        """
        获取Logger日志器对象
        :return:
        """
        return self.case_logger


do_log = HandleLog().get_logger()

if __name__ == '__main__':
    pass
    case_logger = HandleLog().get_logger()
    case_logger.debug("这是debug日志")
    case_logger.info("这是info日志")
    case_logger.warning("这是warning日志")
    case_logger.error("这是error日志")
    case_logger.critical("这是critical日志")
