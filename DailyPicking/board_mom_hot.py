"""
Description:
Author: adolf
Date: 2022-08-17 21:37:01
LastEditTime: 2022-08-17 21:37:01
LastEditors: adolf
"""

import json
import os
from datetime import date

# from pprint import pprint
import akshare as ak
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict

# from itertools import reduce

today = date.today()
today = today.strftime("%Y%m%d")


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

with open("Data/BoardData/ALL_INDUSTRY_BOARD.json") as all_market_code:
    industry_board_name_mapping = json.load(all_market_code)


# 根据行业板块的动量对板块进行选择，选择市场上涨势最强的10个板块
def get_choose_board():
    board_res = {}

    for board_name in board_list:
        (w0, R2) = cal_one_board_mom(board_name)
        print(board_name, w0, R2)
        exit()
        # print(board_name)
        # print(industry_board_name_mapping[board_name.replace(".csv","")])
        # print(w0)
        # print(R2)
        board_res[board_name.replace(".csv", "")] = w0 * R2

    board_res_sort = dict(
        sorted(board_res.items(), key=lambda item: item[1], reverse=True)
    )
    # print(board_res_sort)

    choose_board = list(board_res_sort.keys())[:10]
    choose_board_code = [industry_board_name_mapping[key] for key in choose_board]

    print(choose_board)
    print(choose_board_code)

    return choose_board


choose_board_list = get_choose_board()

# 问财热度排行
stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date=today)
# print(stock_hot_rank_wc_df)

stock_hot_rank = stock_hot_rank_wc_df.set_index(["股票代码"])["序号"].to_dict()
# print(stock_hot_rank)
# exit()
res_df_list = []

# 选择板块中的股票，然后通过问财的热度进行排序
for one_choose_board in choose_board_list:
    stock_board_industry_cons = ak.stock_board_industry_cons_em(symbol=one_choose_board)

    stock_board_industry_cons.rename(columns=ch_eng_mapping_dict, inplace=True)
    stock_board_industry_cons = stock_board_industry_cons[["code", "name", "price"]]
    stock_board_industry_cons["hot_rank"] = stock_board_industry_cons["code"].apply(
        lambda x: stock_hot_rank[x] if x in stock_hot_rank else 9999
    )

    stock_board_industry_cons.sort_values(by="hot_rank", inplace=True)
    # stock_board_industry_cons = stock_board_industry_cons[::-1]
    # print(stock_board_industry_cons)
    # print(stock_board_industry_cons[:5])
    res_df_list.append(stock_board_industry_cons[:5])

    # break
res_df = pd.concat(res_df_list)
res_df.sort_values(by="hot_rank", inplace=True)
res_df.reset_index(drop=True, inplace=True)

res_df = res_df[: len(res_df) // 2]
print(res_df)
