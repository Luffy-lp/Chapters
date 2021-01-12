import os
import logging
from logging.handlers import TimedRotatingFileHandler
from common.settings import LOGGING
from common.COM_path import *

LOG_DIR = "D:/LOG"

file_path = os.path.join(path_LOG_MY, LOGGING.get('log_name'))

def create_logger():
    """创建日志收集器"""
    # 1、创建一个收集器
    mylog = logging.getLogger("lemon")
    mylog.setLevel(LOGGING.get('level'))  # 设置收集日志的等级

    # 2、创建一个输出到文件的输出渠道(按时间轮转),
    fh = TimedRotatingFileHandler(file_path, when='d',
                                  interval=1, backupCount=7,
                                  encoding="utf-8")
    fh.setLevel(LOGGING.get('fh_level'))  # 设置输出等级
    mylog.addHandler(fh)  # 添加到收集器中

    # 3、创建一个输出到控制台的输出渠道
    sh = logging.StreamHandler()
    sh.setLevel(LOGGING.get('sh_level'))  # 设置输出等级
    mylog.addHandler(sh)  # 添加到收集器中

    # 4、设置日志输出格式
    formatter = "%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s"
    mate = logging.Formatter(formatter)

    fh.setFormatter(mate)
    sh.setFormatter(mate)

    return mylog

mylog = create_logger()