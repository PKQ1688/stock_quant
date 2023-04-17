#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/23 15:08
# @Author  : Adolf
# @Site    : 
# @File    : stock_k_data_dask.py
# @Software: PyCharm
import time
import baostock as bs
import pandas as pd
from tqdm import tqdm
from dask.distributed import Client, progress

from pathlib import Path
import shutil

# 对文件夹进行清空处理
dir_path = Path('Data/RealData/hfq/')
if dir_path.exists() and dir_path.is_dir():
    shutil.rmtree(dir_path)
dir_path.mkdir(parents=True, exist_ok=True)

bs.login()

date = "2023-01-20"
# 获取交易日当天的交易股票
stock_df = bs.query_all_stock(date).get_data()


def get_base_k_data(code,start_date ,end_date,frequency):
    if start_date is None:
        start_date = "1990-12-19"
    if end_date is None:
        end_date = date
    if frequency is None:
        frequency = "d"
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,volume,amount,turn,peTTM,pctChg,tradestatus,isST",
        start_date=start_date, end_date=end_date,
        frequency=frequency, adjustflag="1")
    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv("Data/RealData/hfq/" + code + ".csv", index=False)
    return result


# if __name__ == '__main__':
    # # client = Client(n_workers=4)
    #
    # start_time = time.time()
    # # futures = []
    # for index, row in tqdm(stock_df.iterrows(), total=stock_df.shape[0]):
    #     if row['tradeStatus'] == '0' or "bj" in row["code"]:
    #         continue
    #     _code = row['code']
    #     get_base_k_data(_code)
    #     # future = client.submit(get_base_k_data, _code)
    #     # futures.append(future)
    #
    # # progress(futures)
    # print("use time: {}".format(time.time() - start_time))
    # # client.close()
    # bs.logout()
    # get_base_k_data("sh.600570")
