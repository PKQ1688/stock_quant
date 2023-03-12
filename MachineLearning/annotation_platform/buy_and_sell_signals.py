"""
@Author       : adolf adolf1321794021@gmail.com
@Date         : 2023-03-09 21:40:11
@LastEditors  : adolf
@LastEditTime : 2023-03-12 12:46:40
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

st.set_page_config(page_title="股票买卖标注平台", layout="wide")

# 缓存内存
if "code_name" not in st.session_state:
    st.session_state["code_name"] = "600570"

if "end_time" not in st.session_state:
    st.session_state["end_time"] = None


def base_show_fun(code_name, end_time):
    # start_time = datetime.strftime(start_time, '%Y-%m-%d')
    end_time = datetime.strftime(end_time, "%Y-%m-%d")

    show_data = show_data_from_df(
        f"Data/RealData/hfq/{code_name}.csv", end_date=end_time
    )
    chart = draw_chart(show_data)
    st_pyecharts(chart, height="600%", width="100%")

    trade_result = st.radio(label="操作", options=["买", "卖", "保持"])
    next_button = st.button("next day")

    return trade_result, next_button, show_data


st.title("买卖信号标注平台")


label_tab, dataset_tab = st.tabs(["Label", "Dataset"])

code_list = os.listdir("Data/RealData/hfq")

with label_tab:
    randpm_code = st.button("随机股票")
    if randpm_code:
        st.session_state["code_name"] = random.choice(code_list).split(".")[0]
    st.write(f'股票代码:{st.session_state["code_name"]}')

    # start_time = st.date_input("开始时间", value=pd.to_datetime("2019-01-01"))
    if st.session_state["end_time"] is None:
        st.session_state["end_time"] = st.date_input("结束时间", value=pd.to_datetime("2020-01-01"))
    

    trade_result, next_button, show_data = base_show_fun(st.session_state["code_name"], st.session_state["end_time"])

    if next_button:
        with open("Data/LabelData/total_dataset.tsv", "a") as f:
            save_data = []
            save_data.append(st.session_state["code_name"])
            save_data.append(show_data["times"][0])
            save_data.append(show_data["times"][-1])
            save_data.append(trade_result)
            line = "\t".join(save_data)
            f.write(f"{line}\n")

        st.session_state["end_time"] = st.session_state["end_time"] + timedelta(days=1)
        st.success("保存成功", icon="✅")

with dataset_tab:
    # pass
    rank_texts_list = []
    with open("Data/LabelData/total_dataset.tsv", "r", encoding="utf8") as f:
        for i, line in enumerate(f.readlines()):
            texts = line.strip().split("\t")
            rank_texts_list.append(texts)
    df = pd.DataFrame(
        np.array(rank_texts_list),
        columns=(["code", "start_time", "end_time", "trade_result"]),
    )
    st.dataframe(df, use_container_width=True)
