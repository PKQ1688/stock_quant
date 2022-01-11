# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/22 22:29
# @Author  : Adolf
# @File    : base_back_trader.py
# @Function:
import itertools
# from functools import reduce

import pandas as pd
import os
# from tqdm import tqdm

import json

import pandas_ta as ta

from Utils.base_utils import get_module_logger
from BackTrader.position_analysis import BaseTransactionAnalysis

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_rows', None)


class TradeStructure:

    def __init__(self, config):
        self.config = config

        self.logger = get_module_logger(module_name="Trade",
                                        level=config["log_level"], )

        self.logger.debug("Trade is begging ......")

        self.trade_rate = 1.5 / 1000
        self.data = None
        self.transaction_analysis = BaseTransactionAnalysis(logger=self.logger)

    @staticmethod
    def init_one_transaction_record(asset_name):
        return {
            "pos_asset": asset_name,
            "buy_date": "",
            "buy_price": 1,
            "sell_date": "",
            "sell_price": 1,
            "holding_time": 0
        }

    def load_dataset(self, data_path, start_stamp=None, end_stamp=None):
        df = pd.read_csv(data_path)
        df["market_cap"] = (df["amount"] * 100 / df["turn"]) / pow(10, 8)

        if start_stamp is not None:
            df = df[df["date"] > start_stamp]

        if end_stamp is not None:
            df = df[df["date"] < end_stamp]

        df.reset_index(drop=True, inplace=True)

        # self.logger.debug(df)
        self.data = df

    def cal_base_technical_indicators(self, sma_list=(5, 10, 20), macd_parm=(12, 26, 9)):
        if sma_list is not None:
            for sma_parm in sma_list:
                self.data["sma" + str(sma_parm)] = ta.sma(self.data["close"],
                                                          length=sma_parm)
        if macd_parm is not None:
            macd_df = ta.macd(close=self.data['close'],
                              fast=macd_parm[0],
                              slow=macd_parm[1],
                              signal=macd_parm[2])

            self.data['macd'], self.data['histogram'], self.data['signal'] = \
                [macd_df['MACD_12_26_9'], macd_df['MACDh_12_26_9'], macd_df['MACDs_12_26_9']]

    def cal_technical_indicators(self, indicators_config):
        raise NotImplementedError

    def trading_algorithm(self):
        raise NotImplementedError

    def strategy_execute(self):
        asset_name = self.data.name[0]
        one_transaction_record = self.init_one_transaction_record(asset_name=asset_name)

        transaction_record_list = []
        self.logger.debug(one_transaction_record)

        for index, trading_step in self.data.iterrows():
            # self.logger.debug(trading_step)

            if trading_step["trade"] == "BUY" and one_transaction_record["buy_date"] == "":
                one_transaction_record["buy_date"] = trading_step["date"]
                one_transaction_record["buy_price"] = trading_step["close"]
                one_transaction_record["holding_time"] = -index

            if trading_step["trade"] == "SELL" and one_transaction_record["buy_date"] != "":
                one_transaction_record["sell_date"] = trading_step["date"]
                one_transaction_record["sell_price"] = trading_step["close"]
                one_transaction_record["holding_time"] += index

                transaction_record_list.append(one_transaction_record.copy())
                one_transaction_record = self.init_one_transaction_record(asset_name=asset_name)

        # self.logger.info(transaction_record_list)
        transaction_record_df = pd.DataFrame(transaction_record_list)

        transaction_record_df["pct"] = (transaction_record_df["sell_price"] / transaction_record_df["buy_price"]) * (
                1 - self.trade_rate) - 1

        self.logger.debug(transaction_record_df)

        return transaction_record_df

    def show_one_stock(self):
        pass

    def run_one_stock_once(self, code_name, indicators_config=None) -> None:

        if indicators_config is None:
            indicators_config = self.config["strategy_params"]

        data_path = os.path.join("Data/RealData/hfq/", code_name + ".csv")

        self.load_dataset(data_path=data_path,
                          start_stamp=self.config["start_stamp"],
                          end_stamp=self.config["end_stamp"])

        if not self.cal_technical_indicators(indicators_config):
            return False

        self.trading_algorithm()
        transaction_record_df = self.strategy_execute()

        asset_analysis = self.transaction_analysis.cal_asset_analysis(self.data)
        if asset_analysis is not None:
            self.logger.info("对标的进行分析:\n{}".format(asset_analysis))

        strategy_analysis = self.transaction_analysis.cal_trader_analysis(transaction_record_df)

        self.logger.info("策略使用的参数:\n{}".format(indicators_config))
        self.logger.info("对策略结果进行分析:\n{}".format(strategy_analysis))

        return True

    def run_one_stock(self, code_name=None):
        indicators_config = self.config["strategy_params"]
        # self.logger.info(indicators_config)

        if code_name is None:
            code_name = self.config["code_name"]

        # if not self.config["one_param"]:
        #     self.logger.debug(indicators_config)
        # p = {k: list(itertools.permutations(v)) for k, v in indicators_config.items()}
        # for blah in itertools.product()
        # self.logger.info(p)
        try:
            for item in itertools.product(*[value for key, value in indicators_config.items()]):
                self.logger.debug(item)
                one_indicator_config = {list(indicators_config.keys())[index]: item[index]
                                        for index in range(len(list(indicators_config.keys())))}

                self.run_one_stock_once(code_name=code_name, indicators_config=one_indicator_config)

                # break
        except Exception as e:
            self.logger.debug(e)
            self.run_one_stock_once(code_name=code_name)

    def run(self) -> None:
        code_name = self.config["code_name"]
        self.logger.info(code_name)

        if isinstance(code_name, list):
            for code in code_name:
                self.run_one_stock(code_name=code)

        elif code_name.upper() == "ALL_MARKET":
            with open("Data/RealData/ALL_MARKET_CODE.json", "r") as all_market_code:
                market_code_dict = json.load(all_market_code)

            self.logger.debug(market_code_dict)

            # for code in market_code_list:
            #     self.run_one_stock(code_name=code)

        else:
            self.run_one_stock()

        # self.run_one_stock()
# if __name__ == '__main__':
#     trade_structure = TradeStructure(config="")
#     trade_structure.run_one_stock(code_name="600570", start_stamp="2021-01-01", end_stamp="2021-12-31")
