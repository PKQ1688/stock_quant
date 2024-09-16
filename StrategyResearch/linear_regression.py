"""
Description: 
Author: adolf
Date: 2022-08-01 21:05:06
LastEditTime: 2022-08-08 23:57:07
LastEditors: adolf
"""
import sys
import json
import numpy as np
import pandas as pd
from loguru import logger
from tqdm.auto import tqdm

from sklearn.linear_model import LinearRegression

# from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, median_absolute_error

# from GetBaseData.hanle_data_show import show_data_from_df
# from Utils.ShowKline.base_kline import draw_chart

# import matplotlib.pyplot as plt
import ray
import psutil
from functools import reduce

pd.set_option("display.max_columns", None)

ray.init(num_cpus=psutil.cpu_count(logical=False))

logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
handler_id = logger.add(sys.stderr, level="debug".upper())  # 添加一个可以修改控制的handler

board_data_path = "Data/BoardData/"

with open(board_data_path + "ALL_INDUSTRY_BOARD.json", "r") as f:
    board_dict = json.load(f)

board_list = list(board_dict.keys())


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def cal_one_date_mom(origin_data, period=20):
    x = np.linspace(0, 1, period).reshape(-1, 1)

    logger.debug(origin_data)

    y = origin_data.values.reshape(-1, 1)

    y = normalization(y)
    # 线性回归
    model = LinearRegression()

    # 岭回归
    # model = Ridge(alpha=1.0, fit_intercept=True)
    # Lasso回归
    # model = Lasso(alpha=1.0, fit_intercept=True)
    model.fit(x, y)

    # yFit = model.predict(x)

    # 输出回归结果 XUPT
    # print('回归截距: w0={}'.format(model.intercept_[0]))  # w0: 截距
    # print('回归系数: w1={}'.format(model.coef_[0][0]))  # w1,..wm: 回归系数

    # print('R2 确定系数：{:.4f}'.format(model.score(x, y)))  # R2 判定系数
    # print('均方误差：{:.4f}'.format(mean_squared_error(y, yFit)))  # MSE 均方误差
    # print('平均绝对值误差：{:.4f}'.format(mean_absolute_error(y, yFit)))  # MAE 平均绝对误差
    # print('中位绝对值误差：{:.4f}'.format(median_absolute_error(y, yFit)))  # 中值绝对误差

    # return (model.coef_[0][0], model.score(x, y))
    return model.coef_[0][0]


# one_board = "汽车零部件"
@ray.remote
def cal_linear_regression(board_name):
    df = pd.read_csv(board_data_path + "industry_origin/{}.csv".format(board_name))

    # df = df[-100:]

    df = df[["date", "open", "close", "high", "low", "volume"]]
    df["mid"] = (df["open"] + df["close"] + df["high"] + df["low"]) / 4

    logger.info(df)
    time_period = 20

    df["line_w"] = (
        df["close"]
        .rolling(window=time_period)
        .apply(lambda x: cal_one_date_mom(x, time_period))
    )
    # df['line_w'], df['line_R2'] = zip(*df['close'].rolling(
    # window=time_period).apply(lambda x: cal_one_date_mom(x, time_period)))

    df = df[["date", "close", "line_w"]]
    df.rename(
        columns={
            "close": "{}_close".format(board_name),
            "line_w": "{}_mom".format(board_name),
        },
        inplace=True,
    )

    logger.info(df)
    # logger.debug(x)
    # logger.debug(y)

    return df


def get_all_data():
    # board_list = board_list[:10]
    futures = [cal_linear_regression.remote(board) for board in board_list]

    def to_iterator(obj_ids):
        while obj_ids:
            done, obj_ids = ray.wait(obj_ids)
            yield ray.get(done[0])

    for x in tqdm(to_iterator(futures), total=len(board_list)):
        pass

    futures = ray.get(futures)

    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["date"], how="outer"), futures
    )
    df_merged.sort_values(by=["date"], inplace=True)
    df_merged.reset_index(drop=True, inplace=True)

    # for future in futures:
    # logger.success(future)
    logger.success(df_merged)
    df_merged.to_csv(board_data_path + "/ALL_INDUSTRY_BOARD_HISTORY.csv", index=False)


def choose_what_need(all_df):
    for board_name in board_dict.keys():
        all_df["{}_pct".format(board_name)] = (
            all_df["{}_close".format(board_name)]
            / all_df["{}_close".format(board_name)].shift(1)
            - 1
        )

    for index, row in all_df.iterrows():
        # logger.debug(row)
        tmp_mom = row[
            [
                "{}_mom".format(board_name)
                for board_name in board_list
                if not pd.isna(row["{}_mom".format(board_name)])
            ]
        ]
        tmp_mom = tmp_mom.to_dict()
        tmp_mom = sorted(tmp_mom.items(), key=lambda x: x[1], reverse=True)
        # logger.debug(tmp_mom)
        try:
            all_df.loc[index, "top_mom"] = tmp_mom[0][0]
            all_df.loc[index, "top_mom_pct"] = all_df.loc[
                index + 1, tmp_mom[0][0].replace("_mom", "_pct")
            ]
        except Exception as e:
            logger.warning(e)
        # if index > 100:
        # break

    # logger.info(all_df)

    # all_df['top_mom_pct'] = all_df["{}_pct".format(all_df['top_mom'])].shift(1)

    all_df = all_df[-1000:]
    all_df["strategy_net"] = (1 + all_df["top_mom_pct"]).cumprod()
    logger.info(all_df)


if __name__ == "__main__":
    # cal_linear_regression("汽车零部件")
    all_df_ = pd.read_csv(board_data_path + "/ALL_INDUSTRY_BOARD_HISTORY.csv")
    choose_what_need(all_df_)

    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.plot(x, y, 'o', label="data")  # 原始数据
    # ax.plot(x, yFit, 'r-', label="OLS")  # 拟合数据

    # ax.legend(loc='best')  # 显示图例
    # plt.title('Linear regression by SKlearn (Youcans)')
    # # plt.show()  # YouCans, XUPT
    # plt.savefig('ShowHtml/line.jpg')
