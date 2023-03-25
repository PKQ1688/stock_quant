"""
@Author       : adolf adolf1321794021@gmail.com
@Date         : 2023-03-09 21:40:11
@LastEditors  : adolf
@LastEditTime : 2023-03-12 21:29:22
@FilePath     : /stock_quant/MachineLearning/annotation_platform/buy_and_sell_signals.py
@Description  : 
"""
import os
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd
import akshare as ak
import streamlit as st

from streamlit_echarts import st_pyecharts
from GetBaseData.hanle_data_show import show_data_from_df

from Utils.ShowKline.base_kline import draw_chart

# st.set_page_config(page_title="股票买卖标注平台", layout="wide")

# 缓存内存
if "code_name" not in st.session_state:
    st.session_state["code_name"] = "sh.600570"

if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

if "end_time" not in st.session_state:
    st.session_state["end_time"] = None

if "trade_calendar" not in st.session_state:
    st.session_state[
        "trade_calendar"
    ] = ak.tool_trade_date_hist_sina().trade_date.tolist()

if "account_status" not in st.session_state:
    st.session_state["account_status"] = "cash"


# st.write(st.session_state["trade_calendar"])


def base_show_fun(code_name, start_time):
    start_time = datetime.strftime(start_time, "%Y-%m-%d")

    _show_data = show_data_from_df(
        f"Data/RealData/Baostock/day/{code_name}.csv", start_date=start_time
    )
    chart = draw_chart(_show_data)
    st_pyecharts(chart, height="600%", width="100%")

    if st.session_state["account_status"] == "cash":
        st.write("账户状态：现金")
        _trade_result = st.radio(label="操作", options=["买", "保持"])
        if _trade_result == "买":
            st.session_state["account_status"] = "hold"
    else:
        st.write("账户状态：持仓")
        _trade_result = st.radio(label="操作", options=["卖", "保持"])
        if _trade_result == "卖":
            st.session_state["account_status"] = "cash"

    _next_button = st.button("next day")

    return _trade_result, _next_button, _show_data


def annotation_platform_main():
    st.title("买卖信号标注平台")

    label_tab, dataset_tab = st.tabs(["Label", "Dataset"])

    code_list = os.listdir("Data/RealData/Baostock/day")

    with label_tab:
        random_code = st.button("随机股票")
        if random_code:
            st.session_state["code_name"] = random.choice(code_list).replace(".csv", "")
        st.write(f'股票代码:{st.session_state["code_name"]}')

        if st.session_state["start_time"] is None:
            st.session_state["start_time"] = st.date_input(
                "开始时间",
                value=pd.to_datetime("2019-01-01"),
                max_value=pd.to_datetime("2023-01-01"),
            )

        # if st.session_state["end_time"] is None:
        # st.session_state["end_time"] = st.date_input("结束时间", value=pd.to_datetime("2020-01-01"))

        # while st.session_state["end_time"] not in st.session_state["trade_calendar"]:
        # st.session_state["end_time"] = st.session_state["end_time"] + timedelta(days=1)

        trade_result, next_button, show_data = base_show_fun(
            code_name=st.session_state["code_name"], start_time=st.session_state["start_time"]
        )
        # st.write(show_data)

        # st.write(st.session_state)
        if next_button:
            with open(f"Data/LabelData/{st.session_state['code_name']}.tsv", "a") as f:
                save_data = list()
                save_data.append(st.session_state["code_name"])
                save_data.append(show_data["times"][0])
                save_data.append(show_data["times"][-1])
                save_data.append(trade_result)
                save_data.append(st.session_state["account_status"])
                line = "\t".join(save_data)
                f.write(f"{line}\n")

            st.session_state["end_time"] = st.session_state["end_time"] + timedelta(days=1)
            while st.session_state["end_time"] not in st.session_state["trade_calendar"]:
                st.session_state["end_time"] = st.session_state["end_time"] + timedelta(
                    days=1
                )
            st.success("保存成功", icon="✅")

        refresh = st.button("重开")
        if refresh:
            st.session_state = {}

    with dataset_tab:
        # pass
        rank_texts_list = []
        # 判断一个文件是否存在
        if os.path.exists(f"Data/LabelData/{st.session_state['code_name']}.tsv"):
            with open(
                    f"Data/LabelData/{st.session_state['code_name']}.tsv", "r", encoding="utf8"
            ) as f:
                for i, line in enumerate(f.readlines()):
                    texts = line.strip().split("\t")
                    rank_texts_list.append(texts)
        df = pd.DataFrame(
            np.array(rank_texts_list),
            columns=(["code", "start_time", "end_time", "trade_result", "account_status"]),
        )
        st.dataframe(df, use_container_width=True)


if __name__ == '__main__':
    annotation_platform_main()
