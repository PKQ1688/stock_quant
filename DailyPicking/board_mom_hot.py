"""
Description: 
Author: adolf
Date: 2022-08-17 21:37:01
LastEditTime: 2022-08-17 21:37:01
LastEditors: adolf
"""
import os
import numpy as np
import pandas as pd

import json
from pprint import pprint

from sklearn.linear_model import LinearRegression


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def cal_one_board_mom(board_data_path, period=20):
    data = pd.read_csv("Data/BoardData/industry_origin/" + board_data_path)
    data = data[["date", "open", "high", "low", "close", "volume"]]
    data = data[-period:]
    data.reset_index(drop=True, inplace=True)
    data["mid"] = (data["open"] + data["close"] + data["high"] + data["low"]) / 4

    model = LinearRegression()
    x = np.linspace(0, 1, period).reshape(-1, 1)

    y_close = data.close.values.reshape(-1, 1)
    y_close = normalization(y_close)
    model.fit(x, y_close)

    # print(model.coef_[0][0])
    R2 = model.score(x, y_close)
    # print(data)
    # print(R2)
    return (model.coef_[0][0], R2)


# cal_one_board_mom("汽车整车.csv")

board_list = os.listdir("Data/BoardData/industry_origin")
# print(board_list)

with open("Data/BoardData/ALL_INDUSTRY_BOARD.json", "r") as all_market_code:
    industry_board_name_mapping = json.load(all_market_code)

def get_choose_board():
    board_res = {}

    for board_name in board_list:
        (w0, R2) = cal_one_board_mom(board_name)
        # print(board_name)
        # print(industry_board_name_mapping[board_name.replace(".csv","")])
        # print(w0)
        # print(R2)
        board_res[board_name.replace(".csv", "")] = w0 * R2

    board_res_sort = dict(sorted(board_res.items(), key=lambda item: item[1], reverse=True))
    # print(board_res_sort)

    choose_board = list(board_res_sort.keys())[:10]
    choose_board_code = [industry_board_name_mapping[key] for key in choose_board]

    print(choose_board)
    print(choose_board_code)

    return choose_board

choose_board_list = get_choose_board()