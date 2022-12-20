"""
 Author       : adolf
 Date         : 2022-12-18 22:55:21
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-18 23:15:14
 FilePath     : /stock_quant/StrategyResearch/time_series/CR.py
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure


class Intertwine(TradeStructure):
    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)
        self.logger.debug(self.data.head(30))

        self.data["sma5"] = ta.sma(self.data.close, length=5)
        self.data["sma10"] = ta.sma(self.data.close, length=10)
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
        "CODE_NAME": "600570",
        # "CODE_NAME": "ALL_MARKET_10",
        # "CODE_NAME": ["600570", "002610", "300663"],
        "START_STAMP": "2020-01-01",
        "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {"sma_length": 10, "ema_length": 10},
    }
    strategy = Intertwine(config)
    strategy.run()
