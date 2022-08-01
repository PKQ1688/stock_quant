'''
Description: 
Author: adolf
Date: 2022-08-01 21:05:06
LastEditTime: 2022-08-01 21:13:07
LastEditors: adolf
'''
# import numpy as np
from locale import D_FMT
import pandas as pd
from loguru import logger
from sklearn.linear_model import LinearRegression

from GetBaseData.hanle_data_show import show_data_from_df
from Utils.ShowKline.base_kline import draw_chart

model = LinearRegression()

board_data_path = "Data/BoardData/"

one_board = "汽车零部件"
df = pd.read_csv(board_data_path + "industry_origin/{}.csv".format(one_board))

df = df[["date", "open", "close", "high", "low", "volume"]]

logger.info(df)

show_data = show_data_from_df(df)
draw_chart(show_data,show_html_path="ShowHtml/CandleChart.html")
