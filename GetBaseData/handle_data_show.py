#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant
# @Date    : 2022/1/6 17:09
# @Author  : Adolf
# @File    : handle_data_show.py
import pandas as pd
from loguru import logger

from Utils.TechnicalIndicators.basic_indicators import MACD

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


def show_data_from_df(
    df_or_dfpath: str = None,
    use_all_data: bool = True,
    start_date: str = None,
    end_date: str = None,
):
    if isinstance(df_or_dfpath, pd.DataFrame):
        pass

    elif isinstance(df_or_dfpath, str):
        df_or_dfpath = pd.read_csv(df_or_dfpath)

    else:
        raise ValueError("df_or_dfpath must be str or pd.DataFrame")

    if "MACD" not in df_or_dfpath.columns:
        # print(macd_df)
        # breakpoint()
        df_or_dfpath["DIFF"], df_or_dfpath["DEA"], df_or_dfpath["MACD"] = MACD(
            df_or_dfpath["close"]
        )

    if not use_all_data:
        df_or_dfpath = df_or_dfpath[-300:]

    if start_date is not None:
        df_or_dfpath = df_or_dfpath[df_or_dfpath["date"] >= start_date]

    if end_date is not None:
        df_or_dfpath = df_or_dfpath[df_or_dfpath["date"] <= end_date]

    # df_or_dfpath = df_or_dfpath[-60:]
    # df_or_dfpath = df_or_dfpath[:30]
    datas = [
        list(oclh)
        for oclh in zip(
            df_or_dfpath["open"].tolist(),
            df_or_dfpath["close"].tolist(),
            df_or_dfpath["high"].tolist(),
            df_or_dfpath["low"].tolist(),
        )
    ]
    if "index" in df_or_dfpath:
        df_or_dfpath["date"] = (
            df_or_dfpath["date"] + "_" + df_or_dfpath["index"].map(str)
        )

    # import pdb;pdb.set_trace()
    buy_list = df_or_dfpath["buy"].tolist() if "buy" in df_or_dfpath else []
    sell_list = df_or_dfpath["sell"].tolist() if "sell" in df_or_dfpath else []
    # import pdb; pdb.set_trace()

    return {
        "datas": datas,
        "times": df_or_dfpath["date"].tolist(),
        "vols": df_or_dfpath["volume"].tolist(),
        "macds": df_or_dfpath["MACD"].tolist(),
        "difs": df_or_dfpath["DIFF"].tolist(),
        "deas": df_or_dfpath["DEA"].tolist(),
        "buy": buy_list,
        "sell": sell_list,
    }


if __name__ == "__main__":
    csv_path = "Data/RealData/qfq/600570.csv"
    print(show_data_from_df(df_or_dfpath=csv_path))
    # draw_chart(show_data_from_df(df_or_dfpath=csv_path))
