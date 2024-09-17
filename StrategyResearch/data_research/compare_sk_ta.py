"""
Author       : adolf
Date         : 2022-12-18 14:19:37
LastEditors  : adolf adolf1321794021@gmail.com
LastEditTime : 2022-12-18 17:27:09
FilePath     : /stock_quant/StrategyResearch/data_research/compare_sk_ta.py
"""

import numpy as np
import pandas as pd
import pandas_ta as ta
from sklearn.linear_model import LinearRegression


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def cal_one_board_mom(board_data_path, period=20):
    data = pd.read_csv("Data/BoardData/industry_origin/" + board_data_path)
    data = data[["date", "open", "high", "low", "close", "volume"]]
    data = data[-period:]
    data.reset_index(drop=True, inplace=True)
    # data["mid"] = (data["open"] + data["close"] + data["high"] + data["low"]) / 4

    model = LinearRegression()
    x = np.linspace(0, 1, period).reshape(-1, 1)

    y_close = data.close.values.reshape(-1, 1)
    # y_close = normalization(y_close)
    model.fit(x, y_close)

    # print(model.coef_[0][0])
    R2 = model.score(x, y_close)
    return model.coef_, R2


def use_ta_cal_one_board_mom(board_data_path, period=20):
    data = pd.read_csv("Data/BoardData/industry_origin/" + board_data_path)
    data = data[["date", "open", "high", "low", "close", "volume"]]
    data = data[-period:]
    data.reset_index(drop=True, inplace=True)
    # data["mid"] = (data["open"] + data["close"] + data["high"] + data["low"]) / 4
    data["linreg"] = ta.linreg(data.close, length=period, slope=True)
    return data.tail(1).linreg.values[0]


if __name__ == "__main__":
    print(cal_one_board_mom("汽车整车.csv"))
    print(use_ta_cal_one_board_mom("汽车整车.csv"))
