"""
Description: 
Author: adolf
Date: 2022-07-03 23:11:00
LastEditTime: 2022-08-09 22:38:37
LastEditors: adolf
"""
import sys
import pandas as pd
from loguru import logger
from dataclasses import dataclass


@dataclass
class MarketChooseConfig:
    LOG_LEVEL: str = "DEBUG"


class MarketChoose:
    def __init__(self, *args, **kwargs) -> None:
        self.config = MarketChooseConfig(*args, **kwargs)

        logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
        logger.add(sys.stderr, level=self.config.LOG_LEVEL)  # 添加一个终端输出的内容
        # logger.add("some_file.log", enqueue=True)  #添加一个文件输出的内容
        logger.info("MarketChoose init")

    def get_market_data(self):
        pass

    def cal_one_data(self):
        raise NotImplementedError



