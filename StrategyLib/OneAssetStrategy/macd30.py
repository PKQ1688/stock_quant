import pandas as pd

# import pandas_ta as ta
# from finta import TA
from BackTrader.base_back_trader import TradeStructure


class MACD309Strategy(TradeStructure):
    """ """

    def load_dataset(self, data_path, start_stamp=None, end_stamp=None):
        min30_data_path = data_path.replace(
            "Data/RealData/hfq/", "Data/RealData/Baostock/30min/"
        )
        day_data_path = data_path.replace(
            "Data/RealData/hfq/", "Data/RealData/Baostock/day/"
        )
        self.data = {}
        # self.logger.debug(data_path)
        self.data["30min"] = pd.read_csv(min30_data_path)
        self.data["day"] = pd.read_csv(day_data_path)
        # self.logger.debug((self.data.head()))

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)
        macd_day = TA.MACD(self.data["day"])
        self.data["day"]["MACD"], self.data["day"]["SIGNAL"] = [
            macd_day["MACD"],
            macd_day["SIGNAL"],
        ]
        self.data["day"]["HISTOGRAM_day"] = (
            self.data["day"]["MACD"] - self.data["day"]["SIGNAL"]
        )
        self.data["day"]["sma5"] = ta.sma(self.data["day"]["close"], length=5)
        self.data["day"]["sma10"] = ta.sma(self.data["day"]["close"], length=10)
        self.data["day"]["_5_10"] = round(
            self.data["day"]["sma5"] - self.data["day"]["sma10"], 3
        )
        self.logger.debug(self.data["day"].tail())
        self.data["day"] = self.data["day"][["date", "_5_10", "HISTOGRAM_day"]]
        self.logger.info(self.data["day"].tail(n=20))

        # self.data["30min"]["5_10"] = self.data["30min"]["date"].apply(
        #     lambda x: self.data["day"][self.data["day"].date == x]["5_10"].tolist()[0])
        self.data["30min"] = pd.merge(self.data["30min"], self.data["day"], on="date")
        self.logger.debug(self.data["30min"].tail(n=20))
        # exit()

        macd_df = TA.MACD(self.data["30min"])
        self.data = self.data["30min"]
        self.data["MACD"], self.data["SIGNAL"] = [macd_df["MACD"], macd_df["SIGNAL"]]
        self.data["HISTOGRAM"] = self.data["MACD"] - self.data["SIGNAL"]
        # exit()
        self.logger.info(self.data.tail(n=30))

    def buy_logic(self):
        # self.logger.debug(pformat(self.trade_state, indent=4, width=20))
        # if self.trade_state.trading_step.HISTOGRAM_day >= -0.1 and self.trade_state.trading_step.HISTOGRAM>0:
        if self.trade_state.trading_step.HISTOGRAM_day >= -0.1:
            # if self.trade_state.trading_step._5_10 >= 0 and self.trade_state.trading_step.HISTOGRAM>0:
            # if  self.trade_state.trading_step.HISTOGRAM > 0:
            return True
        return False

    def sell_logic(self):
        # if self.trade_state.trading_step.HISTOGRAM_day <= 0.1 and self.trade_state.trading_step.HISTOGRAM < 0:
        if self.trade_state.trading_step.HISTOGRAM_day <= 0.1:
            # if self.trade_state.trading_step._5_10 <= 0 and self.trade_state.trading_step.HISTOGRAM < 0:

            # if  self.trade_state.trading_step.HISTOGRAM < 0:

            return True
        return False


if __name__ == "__main__":
    config = {
        "RANDOM_SEED": 42,
        "LOG_LEVEL": "INFO",
        # "CODE_NAME": "sh.600006",
        # "CODE_NAME": "ALL_MARKET_10",
        "CODE_NAME": ["sh.600238"],
        # "CODE_NAME": ["sh.603806", "sh.603697", "sh.603700", "sh.600570", "sh.603809","sh.600238"],
        # "START_STAMP": "2020-01-01",
        # "END_STAMP": "2020-12-31",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    strategy = MACD309Strategy(config)
    strategy.run()
