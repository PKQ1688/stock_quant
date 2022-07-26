# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/23 00:02
# @Author  : Adolf
# @File    : base_utils.py
# @Function:
import contextlib
import functools
import logging
import time
import threading

import uuid
import colorlog



log_config = {
    'DEBUG': {
        'level': 10,
        'color': 'purple'
    },
    'INFO': {
        'level': 20,
        'color': 'green'
    },
    'TRAIN': {
        'level': 21,
        'color': 'cyan'
    },
    'EVAL': {
        'level': 22,
        'color': 'blue'
    },
    'WARNING': {
        'level': 30,
        'color': 'yellow'
    },
    'ERROR': {
        'level': 40,
        'color': 'red'
    },
    'CRITICAL': {
        'level': 50,
        'color': 'bold_red'
    }
}


class Logger:
    """
    Default logger in STOCK_QUANT
    Args:
        name(str) : Logger name, default is 'STOCKQUANT'
    """

    def __init__(self, name: str = None, level: str = 'INFO'):
        name = 'STOCKQUANT-{}'.format(uuid.uuid1()) if not name else name
        self.logger = logging.getLogger(name)

        for key, conf in log_config.items():
            logging.addLevelName(conf['level'], key)
            self.__dict__[key] = functools.partial(self.__call__, conf['level'])
            self.__dict__[key.lower()] = functools.partial(self.__call__,
                                                           conf['level'])

        self.format = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)-12s] [%(levelname)4s][%(filename)s -> %(funcName)s line:%(lineno)d]%(reset)s\n'
            '%(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors={
                key: conf['color']
                for key, conf in log_config.items()
            })

        if not self.logger.handlers:
            self.handler = logging.StreamHandler()
            self.handler.setFormatter(self.format)
            self.logger.addHandler(self.handler)

        self.logLevel = level
        if level.upper() == "INFO":
            self.logger.setLevel(logging.INFO)
        elif level.upper() == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level.upper() == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif level.upper() == "ERROR":
            self.logger.setLevel(logging.ERROR)

        self.logger.propagate = False
        self._is_enable = True

    def disable(self):
        self._is_enable = False

    def enable(self):
        self._is_enable = True

    @property
    def is_enable(self) -> bool:
        return self._is_enable

    def __call__(self, log_level: str, msg: str):
        if not self.is_enable:
            return

        self.logger.log(log_level, msg)

    @contextlib.contextmanager
    def use_terminator(self, terminator: str):
        old_terminator = self.handler.terminator
        self.handler.terminator = terminator
        yield
        self.handler.terminator = old_terminator

    @contextlib.contextmanager
    def processing(self, msg: str, interval: float = 0.1):
        """
        Continuously print a progress bar with rotating special effects.
        Args:
            msg(str): Message to be printed.
            interval(float): Rotation interval. Default to 0.1.
        """
        end = False

        def _printer():
            index = 0
            flags = ['\\', '|', '/', '-']
            while not end:
                flag = flags[index % len(flags)]
                with self.use_terminator('\r'):
                    self.info('{}: {}'.format(msg, flag))
                time.sleep(interval)
                index += 1

        t = threading.Thread(target=_printer)
        t.start()
        yield
        end = True

# logger = Logger()

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
