# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/22 22:29
# @Author  : Adolf
# @File    : base_back_trader.py
# @Function:
from functools import reduce
import random

import pandas as pd
import json
import os
from tqdm import tqdm

import pandas_ta as ta

from Utils.base_utils import get_module_logger

pd.set_option("expand_frame_repr", False)


class TradeStructure:

    def __init__(self, logger_level="INFO"):
        self.logger = get_module_logger(module_name="Trade", level=logger_level)
        self.logger.info("Trade is begging ......")

        self.trade_rate = 1.5 / 1000
        self.pos_tracking = []

    @staticmethod
    def init_one_pos_record(asset_name="empty"):
        pass

    def load_dataset(self, data_path, start_stamp=None, end_stamp=None):
        df = pd.read_csv(data_path)
        df["market_cap"] = (df["amount"] * 100 / df["turn"]) / pow(10, 8)

        if start_stamp is not None:
            df = df[df["date"] > start_stamp]

        if end_stamp is not None:
            df = df[df["date"] < end_stamp]

        df.reset_index(drop=True, inplace=True)

        self.logger.debug(df)

        return df

    def base_technical_index(self, ma_list=(5, 10, 20, 30, 60), ma_parm=(5, 10, 20), macd_parm=(12, 26, 9),
                             kdj_parm=(9, 3)):
        pass

    def cal_technical_index(self, data):
        pass

    def strategy_exec(self):
        pass

    def turn_strategy_exec(self, data):
        pass

    @staticmethod
    def handle_bs_point(df):
        return df

    def eval_index(self, print_log=False):
        pass

    def eval_turn_strategy(self, print_log=False):
        pass

    def run_one_stock(self, code_name, start_stamp=None, end_stamp=None):
        data_path = os.path.join("data/real_data/hfq/", code_name + ".csv")

        data = self.load_dataset(data_path=data_path, start_stamp=start_stamp, end_stamp=end_stamp)

        self.cal_technical_index(data)

    def run_all_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        pass

    def turn_asset_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        pass


if __name__ == '__main__':
    trade_structure = TradeStructure(logger_level="DEBUG")
    trade_structure.run_one_stock(code_name="600570", start_stamp="2021-01-01", end_stamp="2021-12-31")
