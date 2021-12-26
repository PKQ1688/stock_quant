# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/22 22:29
# @Author  : Adolf
# @File    : base_back_trader.py
# @Function:
import logging
from functools import reduce
import random

import pandas as pd
import mplfinance as mpf
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

        self.data = None

    @staticmethod
    def init_one_pos_record(asset_name="empty"):
        pass

    def load_dataset(self, data_path, start_stamp=None, end_stamp=None):
        df = pd.read_csv(data_path)
        df["market_cap"] = (df["amount"] * 100 / df["turn"]) / pow(10, 8)

        self.logger.debug(df)

        if start_stamp is not None:
            pass

        if end_stamp is not None:
            pass

        return df

    def base_technical_index(self, ma_parm=(5, 10, 20), macd_parm=(12, 26, 9), kdj_parm=(9, 3)):
        pass

    def cal_technical_index(self):
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

    def run_one_stock(self, code_name, start_stamp, end_stamp):
        data_path = os.path.join("data/real_data/hfq/", code_name + ".csv")

        self.data = self.load_dataset(data_path=data_path)

    def run_all_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        pass

    def turn_asset_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        pass


if __name__ == '__main__':
    trade_structure = TradeStructure(logger_level="DEBUG")
    trade_structure.run_one_stock(code_name="600570")
