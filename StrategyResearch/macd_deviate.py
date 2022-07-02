'''
Description: 
Author: adolf
Date: 2022-07-02 14:18:51
LastEditTime: 2022-07-02 16:13:39
LastEditors: adolf
'''
import pandas as pd
from finta import TA
import pandas_ta as pdta
from prometheus_client import Histogram
from tqdm.auto import tqdm

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/RealData/hfq/600570.csv")
print(df[-10:])

res_df = TA.MACD(df,period_fast=12,period_slow=26,signal=9,column="close")
res_df["HISTOGRAM"] = res_df["MACD"] - res_df["SIGNAL"]
# print(res_df[-10:])

df = pd.concat(df,res_df)
print(df[-10:])