"""
 Author       : adolf
 Date         : 2022-12-01 23:29:44
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-12 00:19:25
 FilePath     : /stock_quant/BackTrader/core_trade_logic.py
"""
import pandas as pd
from typing import List
from Utils.base_utils import get_logger
from dataclasses import dataclass, field

from .position_analysis import BaseTransactionAnalysis


@dataclass
class OneTransactionRecord:
    pos_asset: str = field(default=None, metadata={"help": "持仓资产"})
    buy_date: str = field(default=None, metadata={"help": "买入时间"})
    buy_price: float = field(default=0.0, metadata={"help": "买入价格"})
    sell_date: str = field(default=None, metadata={"help": "卖出时间"})
    sell_price: float = field(default=0.0, metadata={"help": "卖出价格"})
    holding_time: int = field(default=0, metadata={"help": "持仓时间"})
    take_profit: float = field(default=None, metadata={"help": "止盈价格"})
    stop_loss: float = field(default=None, metadata={"help": "止损价格"})


@dataclass
class TradeStructure:
    trading_step: pd.Series = field(default=None, metadata={"help": "当前交易标的物的状态"})
    one_transaction_record: OneTransactionRecord = field(
        default=None, metadata={"help": "当前交易记录"}
    )
    history_trading_step: List[pd.Series] = field(
        default=None, metadata={"help": "历史交易记录"}
    )

    # def __post_init__(self):
    #     self.one_transaction_record = OneTransactionRecord()
    #     self.history_trading_step = []

class CoreTradeLogic:
    def __init__(self) -> None:
        self.trade_rate = 1.5 / 1000

        self.logger = get_logger(
            level=self.config.LOG_LEVEL, console=True, logger_file=None
        )

        self.trade_state = TradeStructure()
        # 针对交易结果进行分析
        self.transaction_analysis = BaseTransactionAnalysis(logger=self.logger)

    def buy_logic(self):
        raise NotImplementedError

    def sell_logic(self):
        raise NotImplementedError

    def buy(self, index, trading_step, one_transaction_record):
        self.logger.debug(f"buy {index} {trading_step} {one_transaction_record}")

        one_transaction_record.pos_asset = trading_step.code
        one_transaction_record.buy_date = trading_step.date
        one_transaction_record.buy_price = trading_step.close
        one_transaction_record.holding_time = index

        self.logger.debug(one_transaction_record)
        return one_transaction_record

    def sell(self, index, trading_step, one_transaction_record):
        self.logger.debug(f"sell {index} \n {trading_step} \n {one_transaction_record}")

        one_transaction_record.sell_date = trading_step.date
        one_transaction_record.sell_price = trading_step.close
        one_transaction_record.holding_time = (
            index - one_transaction_record.holding_time
        )

        self.logger.debug(one_transaction_record)
        return one_transaction_record

    def base_trade(self, data) -> List[dict]:
        self.trade_state.one_transaction_record = OneTransactionRecord()

        self.trade_state.history_trading_step = []
        transaction_record_list = []
        # self.logger.debug(one_transaction_record)

        for index, trading_step in data.iterrows():

            if len(self.trade_state.history_trading_step) == 0:
                self.trade_state.history_trading_step.append(trading_step)
                continue

            self.trade_state.trading_step = trading_step
            if (
                self.buy_logic()
                and self.trade_state.one_transaction_record.buy_date is None
            ):
                one_transaction_record = self.buy(
                    index, trading_step, self.trade_state.one_transaction_record
                )
                continue

            if (
                self.sell_logic()
                and self.trade_state.one_transaction_record.buy_date is not None
            ):
                one_transaction_record = self.sell(
                    index, trading_step, self.trade_state.one_transaction_record
                )

                transaction_record_list.append(one_transaction_record)
                self.trade_state.one_transaction_record = OneTransactionRecord()

                # if self.buy_logic(trading_step, one_transaction_record):
                #     one_transaction_record = self.buy(
                #         index, trading_step, one_transaction_record
                #     )

            self.trade_state.history_trading_step.append(trading_step)
            if len(self.trade_state.history_trading_step) > 1:
                self.trade_state.history_trading_step.pop(0)

        self.logger.debug(transaction_record_list)
        transaction_record_df = pd.DataFrame(transaction_record_list)
        self.logger.debug(transaction_record_df)

        if len(transaction_record_df) == 0:
            return transaction_record_df

        transaction_record_df["pct"] = (
            transaction_record_df["sell_price"] / transaction_record_df["buy_price"]
        ) * (1 - self.trade_rate) - 1

        self.logger.info(transaction_record_df)

        return transaction_record_df
