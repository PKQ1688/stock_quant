"""
 Author       : adolf
 Date         : 2022-12-11 16:42:58
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-13 23:58:01
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/Demark9.py
"""
import pandas as pd
import pandas_ta as ta

from BackTrader.base_back_trader import TradeStructure


class Demark9Strategy(TradeStructure):
    """
    使用Demark9策略进行交易
    """

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)

        return_demark = ta.td_seq(self.data.close,asint=True,show_all=False)
        self.data = pd.concat([self.data, return_demark], axis=1)  

        self.logger.debug(self.data.head(30))
        show_data = self.data[(self.data["TD_SEQ_UP"]==9) | (self.data["TD_SEQ_DN"]==9)]
        self.logger.info(show_data)
        exit()
        # self.logger.debug(len(self.data))
        # self.logger.debug(len(return_demark))

    def buy_logic(self):
        if self.trade_state.trading_step.TD_SEQ_DN == 9:
            return True
        else:
            return False

    def sell_logic(self):
        if self.trade_state.trading_step.TD_SEQ_UP == 9:
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
        # "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    strategy = Demark9Strategy(config)
    strategy.run()