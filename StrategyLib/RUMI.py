# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/2 17:34
# @Author  : Adolf
# @File    : RUMI.py
# @Function:
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure


class RUMIStrategy(TradeStructure):
    def __init__(self):
        logger_level = "DEBUG"
        super(RUMIStrategy, self).__init__(logger_level=logger_level)

    def cal_technical_indicators(self):
        self.data["sma13"] = ta.sma(self.data["close"], length=13)
        self.data["ema21"] = ta.ema(self.data["close"], length=21)

        self.data["os"] = self.data["sma13"] - self.data["ema21"]

        self.data["aos"] = ta.sma(self.data["os"], length=5)

        # self.logger.info(self.data.tail(30))

    def trading_algorithm(self):
        self.data.loc[(self.data["aos"] > 0) & (self.data["aos"].shift(1) < 0), "trade"] = "BUY"
        self.data.loc[(self.data["aos"] < 0) & (self.data["aos"].shift(1) > 0), "trade"] = "SELL"

        # self.logger.info(self.data.tail(30))


if __name__ == '__main__':
    RUMI_strategy = RUMIStrategy()
    RUMI_strategy.run_one_stock(code_name="600570")
