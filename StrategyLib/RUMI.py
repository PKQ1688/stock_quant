# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/2 17:34
# @Author  : Adolf
# @File    : RUMI_config.py
# @Function:
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.StrategyLibConfig.RUMI_config import rumi_config
# from StrategyLib.StrategyLibConfig.RUMI_params_config import rumi_config


class RUMIStrategy(TradeStructure):
    def __init__(self, config):
        super(RUMIStrategy, self).__init__(config)

    def cal_technical_indicators(self, indicators_config):
        if indicators_config["sma_length"] >= indicators_config["ema_length"]:
            return False

        self.logger.debug(indicators_config)

        self.data["sma"] = ta.sma(self.data["close"], length=indicators_config["sma_length"])
        self.data["ema"] = ta.ema(self.data["close"], length=indicators_config["ema_length"])

        self.data["os"] = self.data["sma"] - self.data["ema"]

        self.data["aos"] = ta.sma(self.data["os"], length=indicators_config["aos_length"])

        return True
        # self.logger.info(self.Data.tail(30))

    def trading_algorithm(self):
        self.data.loc[(self.data["aos"] > 0) & (self.data["aos"].shift(1) < 0), "trade"] = "BUY"
        self.data.loc[(self.data["aos"] < 0) & (self.data["aos"].shift(1) > 0), "trade"] = "SELL"

        # self.logger.info(self.Data.tail(30))


if __name__ == '__main__':
    RUMI_strategy = RUMIStrategy(config=rumi_config)
    # RUMI_strategy.run_one_stock()
    RUMI_strategy.run()
