"""
Description: 
Author: adolf
Date: 2022-08-13 21:45:35
LastEditTime: 2022-08-13 22:02:08
LastEditors: adolf
"""
import pandas as pd
from typing import List
from Utils.base_utils import get_logger
from dataclasses import dataclass

from .position_analysis import BaseTransactionAnalysis


@dataclass
class OneTransactionRecord:
    pos_asset: str = None
    buy_date: str = None
    buy_price: float = 0.0
    sell_date: str = None
    sell_price: float = 0.0
    holding_time: int = 0


class CoreTradeLogic:
    def __init__(self) -> None:
        self.trade_rate = 1.5 / 1000

        self.logger = get_logger(
            level=self.config.LOG_LEVEL, 
            console=True, 
            log_file=None
        )

        # 针对交易结果进行分析
        self.transaction_analysis = BaseTransactionAnalysis(logger=self.logger)

    def buy_logic(self, *args, **kwargs):
        raise NotImplementedError

    def sell_logic(self, *args, **kwargs):
        raise NotImplementedError

    def buy(self, *args, **kwargs):
        raise NotImplementedError

    def sell(self, *args, **kwargs):
        raise NotImplementedError

    def base_trade(self, data) -> List[dict]:
        one_transaction_record = OneTransactionRecord()

        transaction_record_list = []
        # self.logger.debug(one_transaction_record)

        for index, trading_step in data.iterrows():
            if (
                self.buy_logic(trading_step, one_transaction_record)
                and one_transaction_record.buy_date is None
            ):
                one_transaction_record = self.buy(
                    index, trading_step, one_transaction_record
                )

            if (
                self.sell_logic(trading_step, one_transaction_record)
                and one_transaction_record.buy_date is not None
            ):
                one_transaction_record = self.sell(
                    index, trading_step, one_transaction_record
                )

                transaction_record_list.append(one_transaction_record)
                one_transaction_record = OneTransactionRecord()

                if self.buy_logic(trading_step, one_transaction_record):
                    one_transaction_record = self.buy(
                        index, trading_step, one_transaction_record
                    )

        self.logger.debug(transaction_record_list)
        transaction_record_df = pd.DataFrame(transaction_record_list)
        self.logger.debug(transaction_record_df)

        transaction_record_df["pct"] = (
            transaction_record_df["sell_price"] / transaction_record_df["buy_price"]
        ) * (1 - self.trade_rate) - 1

        self.logger.info(transaction_record_df)

        return transaction_record_df
