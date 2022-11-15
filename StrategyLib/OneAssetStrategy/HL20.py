"""
 Author       : adolf
 Date         : 2022-11-15 21:45:01
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-15 23:08:40
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/HL20.py
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy import ma_hl_config


class MaHighLowStrategy(TradeStructure):
    """
    使用20均线的最高价和最低价均线作为买入卖出的依据,具体策略如下:
    1、过去N天的的收盘价高于20最高价均线
    2、收盘价回踩到20最高价均线和20最低价均线之间
    3、收盘价上传20最高价均线买入
    4、均线方向向上
    5、跌破20日最低价均线卖出,盈亏比为1:2
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        self.data["ma20_high"] = ta.sma(
            self.data["high"], length=indicators_config["sma_length"]
        )
        self.data["ma20_low"] = ta.sma(
            self.data["low"], length=indicators_config["sma_length"]
        )

        return True

    def trading_algorithm(self):
        self.data.loc[
            (self.data["sma5"] > self.data["sma10"])
            & (self.data["sma5"].shift(1) < self.data["sma10"].shift(1)),
            "trade",
        ] = "BUY"
        self.data.loc[
            (self.data["sma5"] < self.data["sma10"])
            & (self.data["sma5"].shift(1) > self.data["sma10"].shift(1)),
            "trade",
        ] = "SELL"

        # self.logger.info(self.Data.tail(30))


if __name__ == "__main__":
    ma5ma10_strategy = MaHighLowStrategy(**ma_hl_config)
    ma5ma10_strategy.run()
