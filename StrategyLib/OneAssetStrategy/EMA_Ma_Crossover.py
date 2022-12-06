"""
 Author       : adolf
 Date         : 2022-12-01 22:43:45
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-12-04 23:49:31
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/EMA_Ma_Crossover.py
"""
import pandas_ta as ta
from BackTrader.base_back_trader import TradeStructure


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
        self.data = self.data[
            ["date", "open", "high", "low", "close", "volume", "code"]
        ]

        self.data["ma"] = ta.sma(
            self.data["close"], length=indicators_config["sma_length"]
        )
        self.data["ema"] = ta.ema(
            self.data["close"], length=indicators_config["ema_length"]
        )

        self.data["rsi"] = ta.rsi(self.data["close"])

        self.logger.debug(self.data.tail(30))

    def buy_logic(self, trading_step, one_transaction_record, history_data):
        self.logger.debug(trading_step)
        self.logger.debug(one_transaction_record)
        if (
            trading_step.ma > trading_step.ema
            and trading_step.close > trading_step.open
        ):
            if trading_step.rsi > 50 and trading_step.rsi < 70:
                if trading_step.close > trading_step.ma > trading_step.ema:
                    one_transaction_record.stop_loss = trading_step.ma
                    one_transaction_record.take_profit = (
                        trading_step.close - one_transaction_record.stop_loss
                    ) * 1.5 + trading_step.close
                    return True
        else:
            return False

    def sell_logic(self, trading_step, one_transaction_record):
        self.logger.debug(trading_step)
        self.logger.debug(one_transaction_record)
        if (
            one_transaction_record.take_profit is None
            or one_transaction_record.stop_loss is None
        ):
            return False

        if (
            trading_step.close > one_transaction_record.take_profit
            or trading_step.close < one_transaction_record.stop_loss
        ):
            return True
        else:
            return False


if __name__ == "__main__":
    config = {
        # "RANDOM_SEED": 42,
        "LOG_LEVEL": "SUCCESS",
        # "CODE_NAME": "600570",
        "CODE_NAME": "ALL_MARKET_100",
        # "CODE_NAME": ["600570", "002610", "300663"],
        # "START_STAMP": "2020-01-01",
        # "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        "STRATEGY_PARAMS": {"sma_length": 10, "ema_length": 10},
    }
    strategy = MaEmaCrossover(config)
    strategy.run()
