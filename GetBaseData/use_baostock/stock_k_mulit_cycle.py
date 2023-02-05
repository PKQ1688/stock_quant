"""
 Author       : adolf
 Date         : 2023-02-05 15:45:49
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-02-05 18:24:17
 FilePath     : /stock_quant/GetBaseData/use_baostock/stock_k_mulit_cycle.py
"""
import pandas as pd
import baostock as bs
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
        "date,code,open,high,low,close,volume,amount,turn,peTTM,tradestatus,isST",
        start_date="1990-12-19",
        end_date=last_day,
        frequency=frequency,
        adjustflag="1",
    )
    # 打印结果集
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv("Data/RealData/Baostock/" + file_name + code + ".csv", index=False)


def main():
    bs.login()

    time_cycle = {
        "5": "5min/",
        "15": "15min/",
        "30": "30min/",
        "60": "60min/",
        "d": "day/",
        "w": "week/",
        "m": "month/",
    }

    last_day = "2023-02-03"

    stock_df = bs.query_all_stock(last_day).get_data()
    # print(stock_df)
    code_list = []
    for _, row in stock_df.iterrows():
        if row.code[:6] in ["sh.600", "sh.601", "sh.603", "sh.605", "sz.300", "sz.000"]:
            code_list.append(row.code)
    # print(code_list)
    # print(len(code_list))

    for code_name in tqdm(code_list,total=len(code_list)):
        for frequency in time_cycle.keys():
            file_name = time_cycle[frequency]
            get_base_k_data(
                code=code_name, last_day=last_day, file_name=file_name, frequency=frequency
            )

    bs.logout()


main()