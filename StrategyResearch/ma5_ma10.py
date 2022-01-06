# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/12/19 16:27
# @Author  : Adolf
# @File    : ma5_ma10.py
# @Function:
import pandas as pd
import pandas_ta as ta

from pyecharts.charts import Bar
from pyecharts import options as opts

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/real_data/hfq/600570.csv")

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

df.loc[(df["sma5"] > df["sma10"]) & (df["sma5"].shift(1) < df["sma10"].shift(1)), "trade"] = "BUY"
# df.loc[(df["sma5"] < df["sma10"]) & (df["sma5"].shift(1) > df["sma10"].shift(1)), "trade"] = "SELL"

df = df.loc[df["trade"].notnull() & (df['macd'] > 0) & (df["histogram"] > 0)]
# df.dropna(subset=['trade'], inplace=True)

print(df)

bar = Bar()
bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))

bar.render()
