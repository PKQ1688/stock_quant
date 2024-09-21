# ！/usr/bin/env python
# @Project : stock_quant
# @Date    : 2022/2/5 16:00
# @Author  : Adolf
# @File    : get_history_data.py
# @Function:
# import requests
import time

import baostock as bs
import pandas as pd
from tqdm import tqdm

# import akshare as ak

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

# 历史行情数据
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001",
#                                         period="daily",  # choice of {'daily', 'weekly', 'monthly'}
#                                         start_date="20170301",
#                                         end_date='20210907',
#                                         adjust="qfq")
#
# print(stock_zh_a_hist_df)

# 分时数据
# stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001",
#                                                       # start_date="2021-09-01 09:32:00",
#                                                       # end_date="2021-09-06 09:32:00",
#                                                       period='5',  # choice of {'1', '5', '15', '30', '60'};
#                                                       adjust='qfq')
# # {'', 'qfq', 'hfq'}; '': 不复权, 'qfq': 前复权, 'hfq': 后复权,
# 分时数据只能返回最近的,
# 其中 1 分钟数据返回近 5 个交易日数据且不复权
# TODO 寻找较长时间的分时数据源头

# print(stock_zh_a_hist_min_em_df)

# 指数数据
# stock_zh_index_spot_df = ak.stock_zh_index_spot()
# print(stock_zh_index_spot_df)

# "上证指数", "深证成指", "创业板指", "沪深300","中证500"
# index_list = ["sh000001", "sz399001", "sz399006", "sz399300", "sh000905"]

# stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol="sh000001")
# print(stock_zh_index_daily_tx_df)

# 使用baostock获取数据

lg = bs.login()
date = "2023-01-20"
stock_df = bs.query_all_stock(date).get_data()
# print(stock_df)

# 获取沪深A股历史K线数据
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
# adjustflag 复权状态(1：后复权， 2：前复权，3：不复权）

st_time = time.time()

for index, row in tqdm(stock_df.iterrows(), total=stock_df.shape[0]):
    if row["tradeStatus"] == "0" or "bj" in row["code"]:
        continue
    code = row["code"]
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,volume,amount,turn,peTTM,pctChg,tradestatus,isST",
        start_date="1990-12-19",
        end_date=date,
        frequency="d",
        adjustflag="1",
    )
    # 打印结果集
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv("Data/RealData/hfq/" + code + ".csv", index=False)
    # print(result)
    # break

print("耗时: ", time.time() - st_time)
# 登出系统
bs.logout()
