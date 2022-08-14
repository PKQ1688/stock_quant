"""
Description: 
Author: adolf
Date: 2022-07-05 19:38:38
LastEditTime: 2022-08-14 13:19:09
LastEditors: adolf
"""
from finta import TA
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.OneAssetStrategy import macd_ma_config


class MACDMA60(TradeStructure):
    """
    选股:60日线上  金叉 macd在0轴上方  买点: 第一根绿线 卖点:收益2个点则卖，最晚第三天卖
    """

    def __init__(self, config):
        super(MACDMA60, self).__init__(config)

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug("macd config:{}".format(indicators_config))

        self.data["MA60"] = self.data.close.rolling(60).mean()

        macd_df = TA.MACD(self.data)
        self.data["MACD"], self.data["SIGNAL"] = [macd_df["MACD"], macd_df["SIGNAL"]]
        self.data["HISTOGRAM"] = self.data["MACD"] - self.data["SIGNAL"]

        # 获取到MACD金叉点和死叉点
        self.data.loc[
            (self.data["HISTOGRAM"] > 0) & (self.data["HISTOGRAM"].shift(1) < 0),
            "golden",
        ] = "LONG"
        self.data.loc[
            (self.data["HISTOGRAM"] < 0) & (self.data["HISTOGRAM"].shift(1) > 0),
            "golden",
        ] = "SHORT"

        self.data["state"] = 0
        self.data.loc[
            (self.data["HISTOGRAM"] > 0) & (self.data["close"] > self.data["MA60"]),
            "state",
        ] = 1
        # self.data.loc[self.data['HISTOGRAM']>0,'state'] = 1

        # self.logger.debug(self.data[:30])
        # exit()

    def trading_algorithm(self):
        golden = "SHORT"

        buy_flag = 0
        for index, row in self.data.iterrows():
            # self.logger.debug(row)
            if row["golden"] == "LONG":
                golden = "LONG"
                buy_flag += 1
            elif row["golden"] == "SHORT":
                golden = "SHORT"
            if (
                golden == "LONG"
                and row["state"] == 1
                and row["close"] < row["open"]
                and buy_flag > 0
            ):
                self.data.loc[index, "trade"] = "BUY"
                buy_flag = 0
                # elif row['golden'] == "SHORT":
                if (index + 3) < len(self.data):
                    self.data.loc[index + 3, "trade"] = "SELL"


if __name__ == "__main__":
    MACD_MA_strategy = MACDMA60(config=macd_ma_config)
    MACD_MA_strategy.run()
