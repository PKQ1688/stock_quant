#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant 
# @Date    : 2022/1/6 17:09
# @Author  : Adolf
# @File    : hanle_data_show.py
import pandas as pd
import pandas_ta as ta


def get_show_data(_df):
    if not isinstance(_df, pd.DataFrame):
        _df = pd.read_csv(_df)

    macd_df = ta.macd(close=_df['close'])

    # print(_df)

    # oclh
    datas = [list(oclh) for oclh in
             zip(_df["open"].tolist(), _df["close"].tolist(), _df["high"].tolist(), _df["low"].tolist())]

    times = _df["date"].tolist()
    vols = _df["volume"].tolist()
    macds = macd_df["MACDh_12_26_9"].tolist()
    difs = macd_df["MACD_12_26_9"].tolist()
    deas = macd_df['MACDs_12_26_9'].tolist()

    # print(times)

    # return df.to_dict(orient="list")
    return {
        "datas": datas,
        "times": times,
        "vols": vols,
        "macds": macds,
        "difs": difs,
        "deas": deas,
    }


if __name__ == '__main__':
    csv_path = "Data/RealData/origin/600570.csv"
    df = pd.read_csv(csv_path)
    print(get_show_data(_df=df))
