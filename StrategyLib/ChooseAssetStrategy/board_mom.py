"""
Description:
Author: adolf
Date: 2022-08-09 23:11:43
LastEditTime: 2022-08-09 23:35:59
LastEditors: adolf
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression  # , Ridge, Lasso

from BackTrader.market_choose import MarketChoose


class BoardMoMStrategy(MarketChoose):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.board_data_path = "Data/BoardData/industry_origin/"

        # 线性回归
        self.model = LinearRegression()
        # 岭回归
        # model = Ridge(alpha=1.0, fit_intercept=True)
        # Lasso回归
        # model = Lasso(alpha=1.0, fit_intercept=True)

    @staticmethod
    def normalization(data):
        _range = np.max(data) - np.min(data)
        return (data - np.min(data)) / _range

    def cal_one_date_mom(self, origin_data, period=20):
        """
        计算一天的mom
        :param origin_data: 一天的原始数据
        :param period: mom周期
        """
        x = np.linspace(0, 1, period).reshape(-1, 1)
        y = origin_data.values.reshape(-1, 1)
        y = self.normalization(y)

        self.model.fit(x, y)
        return self.model.coef_[0][0]

    def cal_one_data(self, file_name="", period=20):
        """
        计算一个板块的mom
        :param file_name: 文件名称
        :param period: mom周期
        """
        origin_data = pd.read_csv(self.config.DATA_PATH + file_name)
        data = origin_data[["date", "open", "close", "high", "low", "volume"]].copy()
        data["mid"] = (data["open"] + data["close"] + data["high"] + data["low"]) / 4
        # self.logger.debug(data)

        data["line_w"] = (
            data["close"]
            .rolling(window=period)
            .apply(lambda x: self.cal_one_date_mom(x, period))
        )

        data = data[["date", "close", "line_w"]]
        data.rename(
            columns={
                "close": "{}_close".format(file_name.split(".")[0]),
                "line_w": "{}_mom".format(file_name.split(".")[0]),
            },
            inplace=True,
        )

        # self.logger.success(data)
        return data

    def choose_rule(self, data):
        for index, row in data.iterrows():
            tmp_mom = row[
                [
                    "{}_mom".format(board_name.split(".")[0])
                    for board_name in self.all_data_list
                    if not pd.isna(row["{}_mom".format(board_name.split(".")[0])])
                ]
            ]
            tmp_mom = tmp_mom.to_dict()
            tmp_mom = sorted(tmp_mom.items(), key=lambda x: x[1], reverse=True)

            try:
                # data.loc[index, "top_mom"] = tmp_mom[0][0].replace("_mom", "")
                data.loc[index, "choose_assert"] = tmp_mom[0][0].replace("_mom", "")
                # data.loc[index,"choose_value"] = row[tmp_mom[0][0].replace("_mom", "_close")]
            except Exception as e:
                self.logger.warning(e)

        self.logger.debug(data)

        # data = data[["date", "top_mom", "top_mom_pct"]]
        return data


if __name__ == "__main__":
    import time

    board_mom_strategy = BoardMoMStrategy(
        LOG_LEVEL="DEBUG",
        DATA_PATH="Data/BoardData/industry_origin/",
        SAVE_PATH="Data/ChooseData/board_mom.csv",
        RUN_ONLINE=False,
    )
    local_time = time.time()
    # board_mom_strategy.cal_one_data(board_name="汽车零部件", period=20)
    board_mom_strategy.run()
    print(time.time() - local_time)
