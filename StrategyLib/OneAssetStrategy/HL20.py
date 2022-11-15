import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy import ma_hl_config


class MaHighLowStrategy(TradeStructure):
    """
    5日均线和10日均线策略,当5日均线上穿10日均线时买入,当5日均线下穿10日均线时卖出
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        self.data["ma21_high"] = ta.sma(self.data["high"], length=indicators_config["sma_length"])
        self.data["ma21_low"] = ta.sma(self.data["low"], length=indicators_config["sma_length"])

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