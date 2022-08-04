'''
Description: 
Author: adolf
Date: 2022-08-01 21:05:06
LastEditTime: 2022-08-04 23:47:16
LastEditors: adolf
'''
from cmath import log
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, median_absolute_error

from GetBaseData.hanle_data_show import show_data_from_df
from Utils.ShowKline.base_kline import draw_chart

import matplotlib.pyplot as plt

board_data_path = "Data/BoardData/"

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

one_board = "汽车零部件"
df = pd.read_csv(board_data_path + "industry_origin/{}.csv".format(one_board))

df = df[["date", "open", "close", "high", "low", "volume"]]
df['mid'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4

logger.info(df)

show_data = show_data_from_df(df)
# draw_chart(show_data, show_html_path="ShowHtml/CandleChart.html")
x = np.linspace(0, 1, 20).reshape(-1, 1)
y = df.close.values.reshape(-1, 1)[-20:]
y = normalization(y)

# logger.debug(x)
# logger.debug(y)

# 线性回归
model = LinearRegression()
# 岭回归
# model = Ridge(alpha=1.0, fit_intercept=True)
# Lasso回归
# model = Lasso(alpha=1.0, fit_intercept=True)

model.fit(x, y)

yFit = model.predict(x)

# 输出回归结果 XUPT
print('回归截距: w0={}'.format(model.intercept_))  # w0: 截距
print('回归系数: w1={}'.format(model.coef_))  # w1,..wm: 回归系数

# 回归模型的评价指标 YouCans
print('R2 确定系数：{:.4f}'.format(model.score(x, y)))  # R2 判定系数
print('均方误差：{:.4f}'.format(mean_squared_error(y, yFit)))  # MSE 均方误差
print('平均绝对值误差：{:.4f}'.format(mean_absolute_error(y, yFit)))  # MAE 平均绝对误差
print('中位绝对值误差：{:.4f}'.format(median_absolute_error(y, yFit)))  # 中值绝对误差

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, 'o', label="data")  # 原始数据
ax.plot(x, yFit, 'r-', label="OLS")  # 拟合数据

ax.legend(loc='best')  # 显示图例
plt.title('Linear regression by SKlearn (Youcans)')
# plt.show()  # YouCans, XUPT
plt.savefig('ShowHtml/line.jpg')