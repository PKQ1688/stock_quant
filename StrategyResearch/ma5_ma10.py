# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/19 16:27
# @Author  : Adolf
# @File    : ma5_ma10.py
# @Function:
import pandas as pd
import pandas_ta as ta
from GetBaseData.hanle_data_show import get_show_data
from Utils.ShowKline.base_kline import draw_chart
from tqdm.auto import tqdm

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/RealData/hfq/600570.csv")

# print(df)
# df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)

# df.ta.log_return(cumulative=True, append=True)
# df.ta.percent_return(cumulative=True, append=True)
df["sma5"] = ta.sma(df['close'], length=5)
df["sma10"] = ta.sma(df['close'], length=10)

df["ema10"] = ta.ema(df['close'], length=10)
# print(help(ta.macd))
macd_df = ta.macd(close=df['close'])

df['macd'], df['histogram'], df['signal'] = [macd_df['MACD_12_26_9'], macd_df['MACDh_12_26_9'],
                                             macd_df['MACDs_12_26_9']]
# pd.concat([df, ta.macd(close=df['close'])])

df = df[df["date"] > "2020-01-01"]
df.reset_index(inplace=True, drop=True)

df.loc[(df["sma5"] > df["sma10"]) & (df["sma5"].shift(1) < df["sma10"].shift(1)), "trade"] = "BUY"
# df.loc[(df["sma5"] < df["sma10"]) & (df["sma5"].shift(1) > df["sma10"].shift(1)), "trade"] = "SELL"

# df = df.loc[df["trade"].notnull() & (df['macd'] > 0) & (df["histogram"] > 0)]
df_chose = df.loc[df["trade"].notnull()]
print(df_chose)
progress = tqdm(range(len(df_chose)), desc="test", disable=False)

for show_index in df_chose.index:
    # print(show_index)
    show_df = df[max(0, show_index - 60):min(len(df), show_index + 10)]
    show_data = get_show_data(_df=show_df)
    progress.update(1)

    # draw_chart(show_data, show_html_path="ShowHtml/Ma5Ma10.html")
    # break
# df.dropna(subset=['trade'], inplace=True)

# print(df.tail(10))
