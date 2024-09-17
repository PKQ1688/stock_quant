# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/22 22:29
# @Author  : Adolf
# @File    : base_back_trader.py
# @Function:
import itertools
import json
import os
import random
import statistics
from dataclasses import dataclass, field
from typing import Dict, Optional

# from functools import reduce
import pandas as pd

from BackTrader.core_trade_logic import CoreTradeLogic
from BackTrader.position_analysis import BaseTransactionAnalysis
from GetBaseData.handle_data_show import show_data_from_df
from Utils.ShowKline.base_kline import draw_chart
from Utils.TechnicalIndicators.basic_indicators import MACD, SMA

# from tqdm.auto import tqdm

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)


@dataclass
class TradeStructureConfig:
    LOG_LEVEL: str = field(
        default="INFO",
        metadata={
            "help": "日志级别,默认INFO,可选DEBUG、INFO、WARNING、ERROR、CRITICAL",
        },
    )
    CODE_NAME: Optional[str] = field(default=None, metadata={"help": "股票代码"})
    RANDOM_SEED: int = field(default=42, metadata={"help": "随机种子"})
    STRATEGY_PARAMS: Dict = field(
        default_factory=lambda: dict(), metadata={"help": "策略参数"}
    )
    START_STAMP: str = field(default=None, metadata={"help": "开始时间"})
    END_STAMP: str = field(default=None, metadata={"help": "结束时间"})
    SHOW_DATA_PATH: str = field(default=None, metadata={"help": "展示数据路径"})


class TradeStructure(CoreTradeLogic):
    def __init__(self, config):
        self.config = TradeStructureConfig(**config)
        super().__init__()

        self.logger.info("Trade is begging ......")

        self.data = None
        self.transaction_analysis = BaseTransactionAnalysis(logger=self.logger)

        self.stock_result = None
        self.pl_result = None

        # 设置随机种子，保证实验结果的可复现性
        random.seed(self.config.RANDOM_SEED)

    # 加载数据集
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
        self.data = self.data[
            [
                "date",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "turn",
                "market_cap",
                "code",
            ]
        ]

    # 计算基础的交易指标
    def cal_base_technical_indicators(
        self, sma_list=(5, 10, 20), macd_parm=(12, 26, 9)
    ):
        if sma_list is not None:
            for sma_parm in sma_list:
                self.data["sma" + str(sma_parm)] = SMA(
                    self.data["close"], timeperiod=sma_parm
                )
        if macd_parm is not None:
            macd_df = MACD(
                close=self.data["close"],
                fastperiod=macd_parm[0],
                slowperiod=macd_parm[1],
                signalperiod=macd_parm[2],
            )

            self.data["macd"], self.data["histogram"], self.data["signal"] = [
                macd_df["MACD_12_26_9"],
                macd_df["MACDh_12_26_9"],
                macd_df["MACDs_12_26_9"],
            ]

    # 计算需要使用到的指标
    def cal_technical_indicators(self, indicators_config):
        """可以计算需要用到的指标，如果不重写则使用默认的指标"""
        self.cal_base_technical_indicators()
        # raise NotImplementedError

    # 使用的到的交涉策略细节(已废弃)
    # def trading_algorithm(self):
    #     raise NotImplementedError

    # 需要保证show_data里面的核心数据没有空值，不然会造成数据无法显示
    # @staticmethod
    def show_one_stock(self, show_data):
        if not os.path.exists("ShowHtml"):
            os.mkdir("ShowHtml")
        show_data_path = (
            self.config.SHOW_DATA_PATH
            if self.config.SHOW_DATA_PATH
            else "ShowHtml/demo.html"
        )
        show_data = show_data_from_df(df_or_dfpath=show_data)
        # import pdb;pdb.set_trace()
        draw_chart(input_data=show_data, show_html_path=show_data_path)

    # 使用一套参数对一只股票进行回测
    def run_one_stock_once(self, code_name, indicators_config=None):
        if indicators_config is None:
            indicators_config = self.config.STRATEGY_PARAMS

        data_path = os.path.join("Data/RealData/hfq/", code_name + ".csv")

        self.load_dataset(
            data_path=data_path,
            start_stamp=self.config.START_STAMP,
            end_stamp=self.config.END_STAMP,
        )

        self.cal_technical_indicators(indicators_config)
        self.data.dropna(
            axis=0, how="any", inplace=True
        )  # drop all rows that have any NaN values
        self.data.reset_index(drop=True, inplace=True)

        # if not self.cal_technical_indicators(indicators_config):
        # return False

        # 废弃了，现在需要编写算法的购买逻辑和卖出逻辑
        # self.trading_algorithm()
        # transaction_record_df = self.strategy_execute()

        transaction_record_df = self.base_trade(self.data)

        asset_analysis = self.transaction_analysis.cal_asset_analysis(self.data)

        if asset_analysis is not None:
            self.logger.success("对标的进行分析:\n{}".format(asset_analysis))
            self.stock_result = asset_analysis

        if len(transaction_record_df) > 0:
            strategy_analysis = self.transaction_analysis.cal_trader_analysis(
                transaction_record_df
            )
        else:
            self.logger.info("没有交易记录，无法进行交易分析")
            return None

        # self.logger.debug("策略使用的参数:\n{}".format(indicators_config))
        # self.logger.debug("对策略结果进行分析:\n{}".format(strategy_analysis))

        self.pl_result = strategy_analysis

        pl_ration = strategy_analysis.loc["策略的盈亏比", "result"]
        # self.logger.info(pl_ration)

        return pl_ration

    def run_one_stock(self, code_name=None):
        pl_ration = 0
        # indicators_config = self.config.get("strategy_params", {})
        indicators_config = self.config.STRATEGY_PARAMS
        # self.logger.info(indicators_config)

        if code_name is None:
            code_name = self.config.CODE_NAME

        # if not self.config["one_param"]:
        #     self.logger.debug(indicators_config)
        # p = {k: list(itertools.permutations(v)) for k, v in indicators_config.items()}
        # for blah in itertools.product()
        # self.logger.info(p)

        if indicators_config:
            if any(
                [isinstance(value, list) for key, value in indicators_config.items()]
            ):
                pl_ration_list = []
                for item in itertools.product(
                    *[value for key, value in indicators_config.items()]
                ):
                    self.logger.debug(item)
                    one_indicator_config = {
                        list(indicators_config.keys())[index]: item[index]
                        for index in range(len(list(indicators_config.keys())))
                    }

                    one_pl_relation = self.run_one_stock_once(
                        code_name=code_name, indicators_config=one_indicator_config
                    )
                    # if one_pl_relation is not nan:
                    pl_ration_list.append(one_pl_relation)
                pl_ration = statistics.mean(pl_ration_list)

            else:
                pl_ration = self.run_one_stock_once(code_name=code_name)

        else:
            pl_ration = self.run_one_stock_once(code_name=code_name)

        self.logger.success("{}的盈亏比是{}".format(code_name, pl_ration))
        self.show_one_stock(self.data)

        return pl_ration

    def run(self) -> None:
        code_name = self.config.CODE_NAME
        self.logger.debug(code_name)

        pl_ration_list = []
        if isinstance(code_name, list):
            for code in code_name:
                one_pl_ration = self.run_one_stock(code_name=code)
                pl_ration_list.append(one_pl_ration)
            pl_ration = statistics.mean(pl_ration_list)

        # elif code_name.upper() == "ALL_MARKET":
        elif "ALL_MARKET" in code_name.upper():
            with open("Data/RealData/ALL_MARKET_CODE.json", "r") as all_market_code:
                market_code_dict = json.load(all_market_code)
            self.logger.debug(market_code_dict)

            market_code_list = list(market_code_dict.keys())

            if code_name.upper() != "ALL_MARKET":
                sample_num = int(code_name.split("_")[-1])
                market_code_list = random.sample(market_code_list, int(sample_num))

            self.logger.debug(market_code_list)

            for code in market_code_list:
                self.logger.info(code)
                try:
                    one_pl_ration = self.run_one_stock(code_name=code)
                    # self.logger.info(one_pl_ration)

                    # 判断变量是否为nan,如果是nan则不添加进List
                    if not one_pl_ration != one_pl_ration and one_pl_ration is not None:
                        pl_ration_list.append(one_pl_ration)
                    # self.logger.info(pl_ration_list)
                except Exception as e:
                    self.logger.debug(e)
                    self.logger.debug(code)
            pl_ration = statistics.mean(pl_ration_list)

        else:
            pl_ration = self.run_one_stock()

        if pl_ration is not None:
            self.logger.success(
                "策略交易一次的收益的数学期望为：{:.2f}%".format(pl_ration * 100)
            )

        # if len(pl_ration_list) > 0:
        # return pl_ration_list[0]
        # else:
        # return None
        # self.run_one_stock()


# if __name__ == '__main__':
#     trade_structure = TradeStructure(config="")
#     trade_structure.run_one_stock(code_name="600570", start_stamp="2021-01-01", end_stamp="2021-12-31")
