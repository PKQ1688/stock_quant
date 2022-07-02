#!/usr/bin/env python
# -*- coding: UTF-8 -*-"""
# @Project : stock_quant 
# @Date    : 2022/1/10 19:14
# @Author  : Adolf
# @File    : Ma5Ma10.py
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.StrategyLibConfig.Ma5Ma10_config import ma5ma10_config


class Ma5Ma10Strategy(TradeStructure):
    '''
    5日均线和10日均线策略，当5日均线上穿10日均线时买入，当5日均线下穿10日均线时卖出
    '''
    def __init__(self, config):
        super(Ma5Ma10Strategy, self).__init__(config)

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        self.data["sma5"] = ta.sma(self.data["close"], length=5)
        self.data["sma10"] = ta.ema(self.data["close"], length=10)

        macd_df = ta.macd(close=self.data["close"])

        self.data["macd"], self.data["histogram"], self.data["signal"] = [macd_df["MACD_12_26_9"],
                                                                          macd_df["MACDh_12_26_9"],
                                                                          macd_df["MACDs_12_26_9"]]

        self.data["atr"] = ta.atr(high=self.data["high"], low=self.data["low"], close=self.data["close"],
                                  length=14)

        # self.logger.debug(help(ta.psar))

        sar_df = ta.psar(high=self.data["high"], low=self.data["low"], close=self.data["close"])

        self.logger.debug(sar_df[:200])

        self.data["long"], self.data["short"], self.data["af"], self.data["reversal"] = [sar_df["PSARl_0.02_0.2"],
                                                                                         sar_df["PSARs_0.02_0.2"],
                                                                                         sar_df["PSARaf_0.02_0.2"],
                                                                                         sar_df["PSARr_0.02_0.2"]]
        # self.logger.info(self.data.tail(30))

        return True

    def trading_algorithm(self):
        self.data.loc[(self.data["sma5"] > self.data["sma10"]) & (
                self.data["sma5"].shift(1) < self.data["sma10"].shift(1)), "trade"] = "BUY"
        self.data.loc[(self.data["sma5"] < self.data["sma10"]) & (
                self.data["sma5"].shift(1) > self.data["sma10"].shift(1)), "trade"] = "SELL"

        # self.logger.info(self.Data.tail(30))


if __name__ == "__main__":
    ma5ma10_strategy = Ma5Ma10Strategy(config=ma5ma10_config)
    ma5ma10_strategy.run()
