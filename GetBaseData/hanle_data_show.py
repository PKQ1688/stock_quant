#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant 
# @Date    : 2022/1/6 17:09
# @Author  : Adolf
# @File    : hanle_data_show.py
import pandas as pd
import pandas_ta as ta

def get_show_data(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.read_csv(df)

    macd_df = ta.macd(close=df['close'])
    # help(ta.macd)
    # df['macd'], df['histogram'], df['signal'] = [macd_df['MACD_12_26_9'], macd_df['MACDh_12_26_9'],
    #                                              macd_df['MACDs_12_26_9']]

    # oclh
    datas = []
    times = df["date"].tolist()
    vols = df["volume"].tolist()
    macds = macd_df["MACDh_12_26_9"].tolist()
    difs = macd_df["MACD_12_26_9"].tolist()
    deas = macd_df['MACDs_12_26_9'].tolist()

    print(times)

    return df.to_dict(orient="list")


if __name__ == '__main__':
    csv_path = "Data/RealData/origin/600570.csv"
    df = pd.read_csv(csv_path)
    get_show_data(df=df)
