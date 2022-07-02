'''
Description: 
Author: adolf
Date: 2022-07-02 14:18:51
LastEditTime: 2022-07-02 22:58:54
LastEditors: adolf
'''
from matplotlib import use
import numpy as np
import pandas as pd

from finta import TA
from sympy import re
from tqdm.auto import tqdm
from scipy.signal import argrelextrema

from Utils.ShowKline.base_kline import draw_chart

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/RealData/hfq/002610.csv")
# print(df[-200:])

res_df = TA.MACD(df,period_fast=12,period_slow=26,signal=9,column="close")
res_df["HISTOGRAM"] = res_df["MACD"] - res_df["SIGNAL"]
# print(res_df[-10:])

df = pd.concat([df,res_df],axis=1)
use_df = df[-200:]
use_df = use_df[['date','close','code','MACD','SIGNAL','HISTOGRAM']]
# print(use_df)
use_df['state'] = 0
# print(df[-10:])
# 获取macd的极大值
# res = argrelextrema(np.array(use_df['HISTOGRAM']),np.greater)[0].tolist()
# 获取macd的极小值
res = argrelextrema(np.array(use_df['HISTOGRAM']),np.less)[0].tolist()
print(res)
exit()
use_df.loc[res,'state'] = 1
# print(use_df.iloc[res,'is'])
print(use_df)

# plt.plot(np.array(use_df['HISTOGRAM']))
# plt.scatter(
#     argrelextrema(np.array(use_df['HISTOGRAM']), np.greater),
#     np.array(use_df['HISTOGRAM'])[argrelextrema(np.array(use_df['HISTOGRAM']), np.greater)],
#     c='red'
# )
# plt.show()
