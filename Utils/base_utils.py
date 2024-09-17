# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/23 00:02
# @Author  : Adolf
# @File    : base_utils.py
# @Function:
import sys

import loguru


def get_logger(level="INFO", console=True, logger_file=None):
    """
    :param level: 选择日志的级别，可选trace，debug，info，warning，error，critical
    :param console: 是不进行控制台输出日志
    :param logger_file: 日志文件路径，None则表示不输出日志到文件
    :return:
    """
    logger = loguru.logger
    logger.remove()

    logger_format = """<green>{time:YYYY-MM-DD HH:mm:ss}</green>| <level>{level}</level> | <cyan>{name}</cyan>=><cyan>{function}</cyan>=><cyan>{line}</cyan>\n<level>{message}</level>"""

    if console:
        logger.add(
            sys.stderr,
            format=logger_format,
            colorize=True,
            level=level.upper(),
        )

    # 添加一个文件输出的内容
    # 目前每天一个日志文件，日志文件最多保存7天
    if logger_file is not None:
        logger.add(
            logger_file,
            enqueue=True,
            level=level.upper(),
            encoding="utf-8",
            rotation="00:00",
            retention="7 days",
        )

    return logger


# 指定只运行一次
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


# 指定函数只运行一次
# def run_one_stock_once(once_stock=False):
#     def run_once(f):
#         def wrapper(*args, **kwargs):
#             if not wrapper.has_run:
#                 wrapper.has_run = True
#                 return f(*args, **kwargs)
#
#         wrapper.has_run = once_stock
#         return wrapper
#
#     return run_once
