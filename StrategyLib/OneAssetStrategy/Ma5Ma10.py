"""
 Author       : adolf
 Date         : 2022-12-03 17:59:38
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-03 18:01:50
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/Ma5Ma10.py
"""
"""
Description: 
Author: adolf
Date: 2022-01-11 20:56:59
LastEditTime: 2022-08-14 13:17:09
LastEditors: adolf
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy import ma5ma10_config


class Ma5Ma10Strategy(TradeStructure):
    """
    5日均线和10日均线策略,当5日均线上穿10日均线时买入,当5日均线下穿10日均线时卖出
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        self.data["sma5"] = ta.sma(self.data["close"], length=5)
        self.data["sma10"] = ta.sma(self.data["close"], length=10)
    
    def buy_logic(self, trading_step, one_transaction_record):
        self.logger.debug(trading_step)
        exit()
        if trading_step.sma5 > trading_step.sma10:
            return True
    
    def sell_logic(self, trading_step, one_transaction_record):
        if trading_step.sma5 < trading_step.sma10:
            return True

    # def trading_algorithm(self):
    #     self.data.loc[
    #         (self.data["sma5"] > self.data["sma10"])
    #         & (self.data["sma5"].shift(1) < self.data["sma10"].shift(1)),
    #         "trade",
    #     ] = "BUY"
    #     self.data.loc[
    #         (self.data["sma5"] < self.data["sma10"])
    #         & (self.data["sma5"].shift(1) > self.data["sma10"].shift(1)),
    #         "trade",
    #     ] = "SELL"

    #     # self.logger.info(self.Data.tail(30))


if __name__ == "__main__":
    config = {
        "RANDOM_SEED": 42,
        "LOG_LEVEL": "debug",
        "CODE_NAME": "600570",
        # "CODE_NAME": "ALL_MARKET_100",
        # "CODE_NAME": ["600570", "002610", "300663"],
        # "START_STAMP": "2020-01-01",
        # "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    ma5ma10_strategy = Ma5Ma10Strategy(config)
    ma5ma10_strategy.run()
