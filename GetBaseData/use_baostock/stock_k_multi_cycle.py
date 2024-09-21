"""
 Author       : adolf
 Date         : 2023-02-05 15:45:49
@LastEditors  : adolf
@LastEditTime : 2023-06-10 16:18:11
@FilePath     : /stock_quant/GetBaseData/use_baostock/stock_k_multi_cycle.py
"""

import os

import baostock as bs
import pandas as pd
from tqdm import tqdm

# import akshare as ak

# 获取 1990-12-19 到 2023-12-29的交易日历
# tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
# print(tool_trade_date_hist_sina_df)


def get_base_k_data(
    code,
    last_day,
    file_name="day",
    frequency="d",
):
    rs = bs.query_history_k_data_plus(
        code,
        # "date,code,open,high,low,close,volume,amount,turn,peTTM,tradestatus,isST",
        "date,code,open,high,low,close,volume,amount",
        # start_date="1990-12-19",
        # end_date=last_day,
        frequency=frequency,
        adjustflag="3",
    )
    # 打印结果集
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 判断是否存在文件夹
    if not os.path.exists("Data/Baostock/" + file_name):
        os.makedirs("Data/Baostock/" + file_name)
    result.to_csv("Data/Baostock/" + file_name + code + ".csv", index=False)


def main():
    bs.login()

    time_cycle = {
        # "5": "5min/",
        # "15": "15min/",
        # "30": "30min/",
        # "60": "60min/",
        "d": "day/",
        # "w": "week/",
        # "m": "month/",
    }

    last_day = "2023-06-10"

    stock_df = bs.query_all_stock(last_day).get_data()
    # print(stock_df)
    code_list = []
    for _, row in stock_df.iterrows():
        if (
            "510300" in row.code
            or "000001" in row.code
            or "399006" in row.code
            or "399106" in row.code
        ):
            print("row.code:", row.code)
            code_list.append(row.code)
        if row.code[:6] in [
            "sh.600",
            "sh.601",
            "sh.603",
            "sh.605",
            "sz.300",
            "sz.000",
            "sz.002",
        ]:
            code_list.append(row.code)
    # print(code_list)
    # print(len(code_list))
    code_list = ["sh.000001", "sz.399001", "sz.399006"]

    for code_name in tqdm(code_list, total=len(code_list)):
        for frequency in time_cycle.keys():
            file_name = time_cycle[frequency]
            get_base_k_data(
                code=code_name,
                last_day=last_day,
                file_name=file_name,
                frequency=frequency,
            )

    bs.logout()


main()
