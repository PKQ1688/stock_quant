"""
 Author       : adolf
 Date         : 2022-12-01 22:43:45
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-02 00:11:20
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/EMA_Ma_Crossover.py
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy import ma_ema_cross_config


class MaEmaCrossover(TradeStructure):
    """
    使用EMA & MA Crossover 和 RSI 进行交易,具体策略如下:
    1、MA > EMA;
    2、close > open
    3、70 > RSI > 50
    4、close > Ma > Ema
    5、stop loss Ma
    6、profit-loss ratio 1:1.5
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)
        self.data = self.data[["date", "open", "high", "low", "close", "volume", "code"]]

        self.data["ma"] = ta.sma(
            self.data["close"], length=indicators_config["sma_length"]
        )
        self.data["ema"] = ta.sma(
            self.data["close"], length=indicators_config["ema_length"]
        )

        self.data["rsi"] = ta.rsi(self.data["close"])

        self.logger.info(self.data.tail(30))
        exit()

    def trading_algorithm(self):
        # TODO: 买入卖出逻辑
        # 需要先对当前策略进行解析才能更好的得出结果
        # self.logger.info(self.Data.tail(30))
        pass


if __name__ == "__main__":
    strategy = MaEmaCrossover(**ma_ema_cross_config)
    strategy.run()
