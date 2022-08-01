#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant 
# @Date    : 2022/1/6 17:09
# @Author  : Adolf
# @File    : hanle_data_show.py
import pandas as pd
from finta import TA
from loguru import logger
# import pandas_ta as ta


# def get_show_data(_df):

#     if isinstance(_df, pd.DataFrame):
#         macd_df = _df[["macd", "histogram", "signal"]]
#         macd_df = macd_df.rename(
#             columns={"macd": "MACD_12_26_9", "histogram": "MACDh_12_26_9", "signal": "MACDs_12_26_9", })
#         # print(macd_df)

#     elif isinstance(_df, str):
#         _df = pd.read_csv(_df)

#         _df = _df[-300:]

#         macd_df = ta.macd(close=_df['close'])
#         macd_df.fillna(0, inplace=True)
#         # print(macd_df)
#         # print(_df)

#     else:
#         macd_df = None

#     # oclh
#     datas = [list(oclh) for oclh in
#              zip(_df["open"].tolist(), _df["close"].tolist(), _df["high"].tolist(), _df["low"].tolist(),
#                  _df["volume"].tolist(), macd_df["MACDh_12_26_9"].tolist(), macd_df["MACD_12_26_9"].tolist(),
#                  macd_df['MACDs_12_26_9'].tolist())]

#     times = _df["date"].tolist()
#     vols = _df["volume"].tolist()
#     macds = macd_df["MACDh_12_26_9"].tolist()
#     difs = macd_df["MACD_12_26_9"].tolist()
#     deas = macd_df['MACDs_12_26_9'].tolist()

#     # print(times)

#     # return df.to_dict(orient="list")
#     return {
#         "datas": datas,
#         "times": times,
#         "vols": vols,
#         "macds": macds,
#         "difs": difs,
#         "deas": deas,
#     }


def show_data_from_df(df_or_dfpath: str=None,use_all_data:bool=False):

    if isinstance(df_or_dfpath, pd.DataFrame):
        try:
            macd_df = df_or_dfpath[["MACD","SIGNAL","HISTOGRAM"]]
        # print(macd_df)
        except:
            macd_df = TA.MACD(df_or_dfpath)
            macd_df["HISTOGRAM"] = macd_df["MACD"] - macd_df["SIGNAL"]

    elif isinstance(df_or_dfpath, str):
        df_or_dfpath = pd.read_csv(df_or_dfpath)

        macd_df = TA.MACD(df_or_dfpath)
        macd_df["HISTOGRAM"] = macd_df["MACD"] - macd_df["SIGNAL"]

        if not use_all_data:
            df_or_dfpath = df_or_dfpath[-300:]
            macd_df = macd_df[-300:]

    else:
        raise ValueError("df_or_dfpath must be str or pd.DataFrame")


    datas = [list(oclh) for oclh in
            zip(df_or_dfpath["open"].tolist(), df_or_dfpath["close"].tolist(), df_or_dfpath["high"].tolist(), df_or_dfpath["low"].tolist())]


    return {
        "datas": datas,
        "times": df_or_dfpath["date"].tolist(),
        "vols": df_or_dfpath["volume"].tolist(),
        "macds": macd_df["HISTOGRAM"].tolist(),
        "difs": macd_df["MACD"].tolist(),
        "deas": macd_df['SIGNAL'].tolist(),
    }


if __name__ == '__main__':
    csv_path = "Data/RealData/qfq/600570.csv"
    print(show_data_from_df(df_or_dfpath=csv_path))
    # draw_chart(show_data_from_df(df_or_dfpath=csv_path))
