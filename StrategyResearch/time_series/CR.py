"""
 Author       : adolf
 Date         : 2022-12-18 22:55:21
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-01-09 22:12:50
 FilePath     : /stock_quant/StrategyResearch/time_series/CR.py
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


class Intertwine(TradeStructure):
    def cal_technical_indicators(self, indicators_config):
        # self.logger.debug(indicators_config)
        # self.logger.debug(self.data.head(30))

        # 计算5日均线和10日均线
        self.data["sma5"] = ta.sma(self.data.close, length=5)
        self.data["sma10"] = ta.sma(self.data.close, length=10)

        # 计算5日均线和10日均线的交叉
        self.data["ma_long"] = ta.cross(self.data.sma5, self.data.sma10)
        self.data["ma_short"] = ta.cross(self.data.sma10, self.data.sma5)

        # 计算macd的值
        self.data[["macd", "histogram", "signal"]] = ta.macd(
            self.data.close, fast=12, slow=26, signal=9
        )

        # 计算bolinger band的值
        self.data[["lower", "mid", "upper", "width", "percent"]] = ta.bbands(
            self.data.close, length=20, std=2
        )

        # 计算atr的值
        self.data["atr"] = ta.atr(
            self.data.high, self.data.low, self.data.close, length=14
        )

        self.data.drop(
            ["signal", "market_cap", "code", "width", "percent"],
            axis=1,
            inplace=True,
        )

        # self.logger.debug(res.tail(30))
        self.logger.debug(self.data.tail(30))

        exit()

        # self.logger.debug(self.data.tail(30))

    def buy_logic(self):
        self.logger.debug(self.trade_state.trading_step)
        self.logger.debug(self.trade_state.one_transaction_record)
        pass

    def sell_logic(self):
        self.logger.debug(self.trade_state.trading_step)
        self.logger.debug(self.trade_state.one_transaction_record)
        pass


if __name__ == "__main__":
    config = {
        # "RANDOM_SEED": 42,
        "LOG_LEVEL": "DEBUG",
        "CODE_NAME": "600519",
        # "CODE_NAME": "ALL_MARKET_10",
        # "CODE_NAME": ["600570", "002610", "300663"],
        "START_STAMP": "2022-01-01",
        # "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {"sma_length": 10, "ema_length": 10},
    }
    strategy = Intertwine(config)
    strategy.run()
