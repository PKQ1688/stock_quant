import pandas as pd
from finta import TA

from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy.macd_30m_dayMacd import MACD30DayMacdStrategy


class MACD30CurMacdStrategy(TradeStructure):
    """ """

    def load_dataset(self, data_path, start_stamp=None, end_stamp=None):
        min30_data_path = data_path.replace(
            "Data/RealData/hfq/", "Data/RealData/Baostock/30min/"
        )
        day_data_path = data_path.replace(
            "Data/RealData/hfq/", "Data/RealData/Baostock/day/"
        )
        self.data = pd.read_csv(min30_data_path)
        self.data = self.data[
            (self.data["date"] >= start_stamp) & (self.data["date"] <= end_stamp)
        ]
        self.data["buy"] = 0
        self.data["sell"] = 0
        self.hist_ratio = 0.005
        self.day_data = pd.read_csv(day_data_path)
        self.day_data = self.day_data[
            (self.day_data["date"] >= start_stamp)
            & (self.day_data["date"] <= end_stamp)
        ]
        self.day_data["index"] = list(range(len(self.day_data)))

        # self.logger.debug((self.data.head()))

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug(indicators_config)
        # macd_day = TA.MACD(self.day_data)
        # self.day_data["MACD"], self.day_data["SIGNAL"] = [macd_day["MACD"], macd_day["SIGNAL"]]
        # self.day_data["HISTOGRAM_day"] = self.day_data['MACD'] - self.day_data['SIGNAL']
        # self.day_data["sma5"] = ta.sma(self.day_data["close"], length=5)
        # self.day_data["sma10"] = ta.sma(self.day_data["close"], length=10)
        # self.day_data["_5_10"] = round(self.day_data["sma5"] - self.day_data["sma10"],3)
        # self.logger.debug(self.day_data.tail())
        # self.day_data=self.day_data[['date','_5_10','HISTOGRAM_day']]
        # self.logger.debug(self.day_data.tail(n=20))
        # self.data=pd.merge(self.data,self.day_data,on="date")
        # self.logger.debug(self.data.tail(n=20))
        # exit()

        macd_df = TA.MACD(self.data)
        self.data["MACD"], self.data["SIGNAL"] = [macd_df["MACD"], macd_df["SIGNAL"]]
        self.data["HISTOGRAM"] = self.data["MACD"] - self.data["SIGNAL"]
        self.data["index"] = list(range(len(self.data)))
        self.data["buy"] = 0
        self.data["sell"] = 0

    def buy_logic(self):
        # 用30分钟的close价格作为日线价格重新计算macd
        self.day_data.loc[
            self.day_data["date"] == self.trade_state.trading_step.date, "close"
        ] = self.trade_state.trading_step.close
        macd_day = TA.MACD(self.day_data)
        self.day_data["MACD_day"], self.day_data["SIGNAL_day"] = [
            macd_day["MACD"],
            macd_day["SIGNAL"],
        ]
        self.day_data["HISTOGRAM_day"] = (
            self.day_data["MACD_day"] - self.day_data["SIGNAL_day"]
        )
        self.day_data["HISTOGRAM_ratio"] = (
            self.day_data["MACD_day"] / self.day_data["SIGNAL_day"]
        )
        allow_diff = self.trade_state.trading_step.close * self.hist_ratio
        cur_index = self.day_data.loc[
            self.day_data["date"] == self.trade_state.trading_step.date, "index"
        ].item()
        new_data = self.day_data[["date", "HISTOGRAM_day", "MACD_day", "SIGNAL_day"]]

        # self.data=pd.merge(self.data,new_data,on="date")

        increase_three_days = False
        if cur_index >= 2:
            increase_three_days = (
                self.day_data.loc[
                    self.day_data["index"] == cur_index, "HISTOGRAM_day"
                ].item()
                > self.day_data.loc[
                    self.day_data["index"] == cur_index - 1, "HISTOGRAM_day"
                ].item()
                > self.day_data.loc[
                    self.day_data["index"] == cur_index - 2, "HISTOGRAM_day"
                ].item()
            )
        if cur_index > 4:
            last_five_list = self.day_data.iloc[cur_index - 4 : cur_index]
        else:
            last_five_list = self.day_data.iloc[:cur_index]
        last_five_avg_val = last_five_list["HISTOGRAM_day"].mean()
        HISTOGRAM_bigger_than = (
            self.day_data.loc[
                self.day_data["date"] == self.trade_state.trading_step.date,
                "HISTOGRAM_day",
            ].item()
            > last_five_avg_val
        )

        # if HISTOGRAM_bigger_than  and increase_three_days \
        #         and self.trade_state.trading_step.HISTOGRAM>=-0:
        # if self.trade_state.trading_step.HISTOGRAM_day >= -0.1 :
        # if self.trade_state.trading_step._5_10 >= 0 and self.trade_state.trading_step.HISTOGRAM>0:
        if (
            self.trade_state.trading_step.HISTOGRAM > 0
            and HISTOGRAM_bigger_than
            and self.day_data.loc[
                self.day_data["index"] == cur_index, "MACD_day"
            ].item()
            > -30
        ):
            #     pdb.set_trace()
            return True
        return False

    def sell_logic(self):
        self.day_data.loc[
            self.day_data["date"] == self.trade_state.trading_step.date, "close"
        ] = self.trade_state.trading_step.close
        macd_day = TA.MACD(self.day_data)
        self.day_data["MACD_day"], self.day_data["SIGNAL_day"] = [
            macd_day["MACD"],
            macd_day["SIGNAL"],
        ]
        self.day_data["HISTOGRAM_day"] = (
            self.day_data["MACD_day"] - self.day_data["SIGNAL_day"]
        )
        self.day_data["HISTOGRAM_ratio"] = (
            self.day_data["MACD_day"] / self.day_data["SIGNAL_day"]
        )
        new_day_data = self.day_data[
            ["date", "HISTOGRAM_day", "MACD_day", "SIGNAL_day"]
        ]

        # self.data=pd.merge(self.data,new_day_data,on="date")

        allow_diff = 0.1
        cur_index = self.day_data.loc[
            self.day_data["date"] == self.trade_state.trading_step.date, "index"
        ].item()
        if cur_index > 3:
            last_five_list = self.day_data.iloc[cur_index - 3 : cur_index]
        else:
            last_five_list = self.day_data.iloc[:cur_index]
        last_five_avg_val = last_five_list["HISTOGRAM_day"].mean()
        HISTOGRAM_smaller_than = (
            self.day_data.loc[
                self.day_data["date"] == self.trade_state.trading_step.date,
                "HISTOGRAM_day",
            ].item()
            < last_five_avg_val
        )
        cur_index = self.day_data.loc[
            self.day_data["date"] == self.trade_state.trading_step.date, "index"
        ].item()
        decrease_three_days = False
        if cur_index >= 2:
            decrease_three_days = (
                self.day_data.loc[
                    self.day_data["index"] == cur_index, "HISTOGRAM_day"
                ].item()
                < self.day_data.loc[
                    self.day_data["index"] == cur_index - 1, "HISTOGRAM_day"
                ].item()
                < self.day_data.loc[
                    self.day_data["index"] == cur_index - 2, "HISTOGRAM_day"
                ].item()
            )

        # if  self.trade_state.trading_step.HISTOGRAM <= 0  and HISTOGRAM_smaller_than and decrease_three_days:
        # if self.trade_state.trading_step.HISTOGRAM_day <= 0.1:

        # if self.trade_state.trading_step._5_10 <= 0 and self.trade_state.trading_step.HISTOGRAM < 0:
        HISTOGRAM_smaller_than = True
        if (
            self.trade_state.trading_step.HISTOGRAM < 0
            and self.day_data.loc[
                self.day_data["index"] == cur_index, "MACD_day"
            ].item()
            < 20
        ):
            #     if self.trade_state.one_transaction_record.buy_date is not None:
            #         self.data.loc[self.data["index"] == self.trade_state.trading_step["index"], "sell"] = 1
            return True
        return False


if __name__ == "__main__":
    config = {
        "RANDOM_SEED": 42,
        "LOG_LEVEL": "INFO",
        "CODE_NAME": "sh.600570",
        # "CODE_NAME": "ALL_MARKET_10",
        # "CODE_NAME": ["sh.600238",],
        # "CODE_NAME": ["sh.603806", "sh.603697", "sh.603700", "sh.600570", "sh.603809","sh.600238","sh.603069","sh.600764","sz.002044"],
        "START_STAMP": "2016-01-01",
        "END_STAMP": "2022-05-23",
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    print(
        "======================macd + day 分割线=====================================分割线==============="
    )
    print(
        "======================macd + day 分割线=====================================分割线==============="
    )

    strategy = MACD30DayMacdStrategy(config)
    strategy.run()

    print(
        "======================30min macd+cur macd分割线=====================================分割线==============="
    )
    print(
        "======================30min macd+cur macd分割线=====================================分割线==============="
    )

    strategy = MACD30CurMacdStrategy(config)
    strategy.run()
