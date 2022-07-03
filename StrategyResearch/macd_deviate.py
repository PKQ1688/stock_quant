'''
Description: 
Author: adolf
Date: 2022-07-02 14:18:51
LastEditTime: 2022-07-03 17:21:58
LastEditors: adolf
'''
import numpy as np
import pandas as pd

from finta import TA
from tqdm.auto import tqdm
from scipy.signal import argrelextrema

# from Utils.ShowKline.base_kline import draw_chart

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/RealData/hfq/002612.csv")

df["30_lowest"] = df.low.rolling(30).min()
# print("30_lowest:",df["30_lowest"])
# exit()
# print(df[-200:])

macd_df = TA.MACD(df,period_fast=12,period_slow=26,signal=9,column="close")
# macd_df = TA.MACD(df,period_fast=13,period_slow=34,signal=9,column="close")

macd_df["HISTOGRAM"] = macd_df["MACD"] - macd_df["SIGNAL"]
# print(res_df[-10:])
# atr_df = TA.ATR(df,period=14)
# print(atr_df[-10:])

# df = pd.concat([df,macd_df,atr_df],axis=1)
df = pd.concat([df,macd_df],axis=1)
df.loc[(df['HISTOGRAM']>0)&(df['HISTOGRAM'].shift(1)<0),'trade'] = "BUY"
df.loc[(df['HISTOGRAM']<0)&(df['HISTOGRAM'].shift(1)>0),'trade'] = "SELL"

use_df = df[-200:]
use_df.reset_index(drop=True, inplace=True)
# print(use_df)
# use_df = use_df[['date','close','code','MACD','SIGNAL','HISTOGRAM',"13 period ATR"]]
use_df = use_df[['date','low','close','code','30_lowest','MACD','SIGNAL','HISTOGRAM','trade']]
# print(use_df)
use_df['price_state'] = 0
price_res = argrelextrema(use_df['low'].values, np.less,order=1)[0].tolist()


last_low_price = None
last_macd = None
for index in price_res:
    # if use_df.loc[index,'low'] == use_df.loc[index,'30_lowest']:
        # use_df.loc[index,'price_state'] = 1

    if last_low_price is not None and last_macd is not None:
        if use_df.loc[index,'low'] < last_low_price and use_df.loc[index,'MACD'] > last_macd and use_df.loc[index,'low'] == use_df.loc[index,'30_lowest']:
            use_df.loc[index,'price_state'] = 1

    last_low_price = use_df.loc[index,'low']
    last_macd = use_df.loc[index,'MACD']

print(use_df)

# print(price_res)
# print(df[-10:])
# 获取macd的极大值
# res = argrelextrema(np.array(use_df['HISTOGRAM']),np.greater)[0].tolist()
# 获取macd的极小值
# res = argrelextrema(np.array(use_df['HISTOGRAM']),np.less)[0].tolist()
# print(res)
# exit()
# for index in res:
    # use_df.loc[index,'state'] = 1 
# print(use_df.iloc[res,'is'])
# use_df_v2 = use_df[(use_df['state']==1) & (use_df['HISTOGRAM']<0)]
# print(use_df_v2)


# plt.plot(np.array(use_df['HISTOGRAM']))
# plt.scatter(
#     argrelextrema(np.array(use_df['HISTOGRAM']), np.greater),
#     np.array(use_df['HISTOGRAM'])[argrelextrema(np.array(use_df['HISTOGRAM']), np.greater)],
#     c='red'
# )
# plt.show()
