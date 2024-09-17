"""
Description:
Author: adolf
Date: 2022-08-14 23:26:03
LastEditTime: 2022-08-15 00:10:45
LastEditors: adolf
"""

import pandas as pd
import pandas_ta as ta

# df = pd.DataFrame()

# print(df.ta.indicators())

# Help about an indicator such as bbands
# help(ta.vp)

df = pd.read_csv("Data/RealData/hfq/000001.csv")

df = df[-1000:]

# print(df)
test = ta.vp(close=df["close"], volume=df["volume"], width=20)
print(test)
