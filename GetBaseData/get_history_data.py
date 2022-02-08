# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/5 16:00
# @Author  : Adolf
# @File    : get_history_data.py
# @Function:
import requests
import pandas as pd

import akshare as ak

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_rows', 1000)

# 历史行情数据
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001",
                                        period="daily",  # choice of {'daily', 'weekly', 'monthly'}
                                        start_date="20170301",
                                        end_date='20210907',
                                        adjust="qfq")

# print(stock_zh_a_hist_df)

# 分时数据
stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001",
                                                      # start_date="2021-09-01 09:32:00",
                                                      # end_date="2021-09-06 09:32:00",
                                                      period='5',  # choice of {'1', '5', '15', '30', '60'};
                                                      adjust='qfq')
# {'', 'qfq', 'hfq'}; '': 不复权, 'qfq': 前复权, 'hfq': 后复权,
# 分时数据只能返回最近的,
# 其中 1 分钟数据返回近 5 个交易日数据且不复权
# TODO 寻找较长时间的分时数据源头

# print(stock_zh_a_hist_min_em_df)

# 指数数据
# stock_zh_index_spot_df = ak.stock_zh_index_spot()
# print(stock_zh_index_spot_df)

# "上证指数", "深证成指", "创业板指", "沪深300","中证500"
index_list = ["sh000001", "sz399001", "sz399006", "sz399300", "sh000905"]

stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol="sh000001")
print(stock_zh_index_daily_tx_df)

