# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/23 00:02
# @Author  : Adolf
# @File    : base_utils.py
# @Function:
import logging


def get_module_logger(module_name, level="INFO"):
    module_name = "quant.{}".format(module_name)

    module_logger = logging.getLogger(module_name)

    if level.upper() == "INFO":
        module_logger.setLevel(logging.INFO)
    elif level.upper() == "DEBUG":
        module_logger.setLevel(logging.DEBUG)
    elif level.upper() == "WARNING":
        module_logger.setLevel(logging.WARNING)
    elif level.upper() == "ERROR":
        module_logger.setLevel(logging.ERROR)

    module_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s :\n %(message)s \n"
        "----------------------------------------------------------------------"
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    module_logger.handlers.append(console_handler)

    return module_logger


# 指定函数只运行一次
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper
