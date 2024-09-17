"""
Author       : adolf
Date         : 2022-12-03 17:59:38
LastEditors  : adolf adolf1321794021@gmail.com
LastEditTime : 2022-12-10 18:02:26
FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/Ma5Ma10.py
"""

from pprint import pformat

from BackTrader.base_back_trader import TradeStructure

# from pyti.simple_moving_average import simple_moving_average as sma
from Utils.TechnicalIndicators.basic_indicators import SMA


class Ma5Ma10Strategy(TradeStructure):
    """
    5日均线和10日均线策略,当5日均线上穿10日均线时买入,当5日均线下穿10日均线时卖出
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        # self.data["sma5"] = ta.sma(self.data["close"], length=5)
        # self.data["sma10"] = ta.sma(self.data["close"], length=10)
        self.data["sma5"] = SMA(self.data["close"], timeperiod=5)
        self.data["sma10"] = SMA(self.data["close"], timeperiod=10)

    # def buy_logic(self, trading_step, one_transaction_record, history_trading_step):
    def buy_logic(self):
        self.logger.debug(pformat(self.trade_state, indent=4, width=20))
        if (
            self.trade_state.trading_step.sma5 > self.trade_state.trading_step.sma10
            and self.trade_state.history_trading_step[0].sma5
            < self.trade_state.history_trading_step[0].sma10
        ):
            return True
        else:
            return False

    def sell_logic(self):
        if (
            self.trade_state.trading_step.sma5 < self.trade_state.trading_step.sma10
            and self.trade_state.history_trading_step[0].sma5
            > self.trade_state.history_trading_step[0].sma10
        ):
            return True
        else:
            return False


if __name__ == "__main__":
    config = {
        "RANDOM_SEED": 42,
        "LOG_LEVEL": "INFO",
        "CODE_NAME": "600570",
        # "CODE_NAME": "ALL_MARKET_100",
        # "CODE_NAME": ["600570", "002610", "300663"],
        "START_STAMP": "2020-01-01",
        "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    strategy = Ma5Ma10Strategy(config)
    strategy.run()
