# -*- coding: UTF-8 -*-
"""
@Project ：stock_quant
@File    ：cal_base_indicators.py
@Author  ：adolf
@Date    ：2023/4/21 22:00
"""

import os

import pandas as pd
from finta import TA

pd.set_option("display.max_columns", None)


def cal_base_indicators(code_path):
    base_data = pd.read_csv("Data/Baostock/day/" + code_path)

    # print(base_data)
    base_data["MA5"] = TA.SMA(base_data, period=5)
    base_data["MA10"] = TA.SMA(base_data, period=10)
    base_data["MA20"] = TA.SMA(base_data, period=20)
    base_data["MA30"] = TA.SMA(base_data, period=30)
    base_data["MA60"] = TA.SMA(base_data, period=60)

    if "HISTOGRAM" not in base_data.columns:
        macd_df = TA.MACD(base_data)
        macd_df["HISTOGRAM"] = macd_df["MACD"] - macd_df["SIGNAL"]
        base_data = pd.concat([base_data, macd_df], axis=1)
    # print(final_data.tail())
    return base_data


code_list = os.listdir("Data/Baostock/day/")
for code in code_list:
    df = cal_base_indicators(code)
    df.to_csv("Data/Baostock/day/" + code, index=False)
    print(code)
