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
from dataclasses import dataclass, field

from functools import reduce
from BackTrader.core_trade_logic import CoreTradeLogic


@dataclass
class MarketChooseConfig:
    LOG_LEVEL: str = field(
        default="INFO",
        metadata={
            "help": "日志级别,默认INFO,可选DEBUG、INFO、WARNING、ERROR、CRITICAL",
        },
    )
    DATA_PATH: str = field(
        default="Data/BoardData/industry_origin", metadata={"help": "数据路径"}
    )
    SAVE_PATH: str = field(
        default="Data/ChooseData/board_mom.csv", metadata={"help": "保存获取完指标路径"}
    )
    RUN_ONLINE: bool = field(default=True, metadata={"help": "是否在线运行,默认为True"})


# @ray.remote
class MarketChoose(CoreTradeLogic):
    def __init__(self, *args, **kwargs) -> None:
        self.config = MarketChooseConfig(*args, **kwargs)
        super().__init__()

        self.logger.info("MarketChoose init")
        self.all_data_list = os.listdir(self.config.DATA_PATH)

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

    def buy_logic(self, *args, **kwargs):
        return True

    def sell_logic(self, trading_step, one_transaction_record, *args, **kwargs):
        if trading_step["choose_assert"] != one_transaction_record.pos_asset:
            return True
        else:
            return False

    def buy(self, index, trading_step, one_transaction_record):
        self.logger.trace(f"buy {index} {trading_step} {one_transaction_record}")

        one_transaction_record.pos_asset = trading_step["choose_assert"]
        one_transaction_record.buy_date = trading_step["date"]
        one_transaction_record.buy_price = trading_step[
            f"{trading_step['choose_assert']}_close"
        ]
        one_transaction_record.holding_time = index

        return one_transaction_record

    def sell(self, index, trading_step, one_transaction_record):
        self.logger.debug(f"sell {index} {trading_step} {one_transaction_record}")

        one_transaction_record.sell_date = trading_step["date"]
        one_transaction_record.sell_price = trading_step[
            f"{one_transaction_record.pos_asset}_close"
        ]
        # one_transaction_record.pos_asset = None
        one_transaction_record.holding_time = (
            index - one_transaction_record.holding_time
        )

        self.logger.debug(one_transaction_record)
        return one_transaction_record
        # self.buy(index, trading_step, one_transaction_record)
        # self.logger.debug(one_transaction_record)
        # exit()

    def run(self):
        if self.config.RUN_ONLINE:
            res_data_list = self.get_market_data()

            df_merged = reduce(
                lambda left, right: pd.merge(left, right, on=["date"], how="outer"),
                res_data_list,
            )
            df_merged.sort_values(by=["date"], inplace=True)
            df_merged.reset_index(drop=True, inplace=True)

            self.logger.success(df_merged)

            choose_data = self.choose_rule(df_merged)
            choose_data.to_csv(self.config.SAVE_PATH, index=False)

        else:
            choose_data = pd.read_csv(self.config.SAVE_PATH)

        # choose_data['choose_assert'].dropna(inplace=True)
        choose_data = choose_data[~pd.isnull(choose_data["choose_assert"])]

        if self.config.LOG_LEVEL == "DEBUG":
            choose_data = choose_data[:100]

        choose_data.reset_index(drop=True, inplace=True)

        self.logger.success(choose_data)

        transaction_record_df = self.base_trade(choose_data)

        pl = self.transaction_analysis.cal_trader_analysis(transaction_record_df)
