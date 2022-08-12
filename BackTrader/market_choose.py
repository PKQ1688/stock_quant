"""
Description: 
Author: adolf
Date: 2022-07-03 23:11:00
LastEditTime: 2022-08-09 22:38:37
LastEditors: adolf
"""
import os
import sys

# import ray
import pathos
import pandas as pd
from loguru import logger
from tqdm.auto import tqdm
from dataclasses import dataclass

from functools import reduce


@dataclass
class MarketChooseConfig:
    LOG_LEVEL: str = "DEBUG"
    DATA_PATH: str = "Data/BoardData/industry_origin"


# @ray.remote
class MarketChoose:
    def __init__(self, *args, **kwargs) -> None:
        self.config = MarketChooseConfig(*args, **kwargs)

        self.logger = logger
        self.logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
        self.logger.add(sys.stderr, level=self.config.LOG_LEVEL)  # 添加一个终端输出的内容
        # logger.add("some_file.log", enqueue=True)  #添加一个文件输出的内容
        self.logger.info("MarketChoose init")

        self.all_data_list = os.listdir(self.config.DATA_PATH)

        # self.data_path = kwargs.get("data_path", "Data/BoardData/industry_origin/")

        # ray.init()

    def get_market_data(self):
        with pathos.multiprocessing.ProcessingPool(8) as p:
            result = list(
                tqdm(
                    p.imap(self.cal_one_data, self.all_data_list),
                    total=len(self.all_data_list),
                    desc="运行全体数据",
                )
            )
        self.logger.success("MarketChoose run success")

        return result

    # @ray.remote
    def cal_one_data(self, *args, **kwargs):
        raise NotImplementedError

    def choose_rule(self, *args, **kwargs):
        raise NotImplementedError

    def run(self):
        res_data_list = self.get_market_data()

        df_merged = reduce(
            lambda left, right: pd.merge(left, right, on=["date"], how="outer"),
            res_data_list,
        )
        df_merged.sort_values(by=["date"], inplace=True)
        df_merged.reset_index(drop=True, inplace=True)

        self.logger.success(df_merged)

        self.choose_rule(df_merged)

        self.logger.trace("only for test")