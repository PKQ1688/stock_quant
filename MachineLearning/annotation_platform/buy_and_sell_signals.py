"""
Author       : adolf adolf1321794021@gmail.com
Date         : 2023-03-05 19:02:48
LastEditors  : adolf
LastEditTime : 2023-03-05 22:39:07
FilePath     : /stock_quant/MachineLearning/annotation_platform/buy_and_sell_signals.py
Description  : 
"""
import numpy as np
import pandas as pd
import streamlit as st

from streamlit_echarts import st_pyecharts
from GetBaseData.hanle_data_show import show_data_from_df

from Utils.ShowKline.base_kline import draw_chart

st.set_page_config(page_title="股票买卖标注平台", layout="wide")

st.title("买卖信号标注平台")

label_tab, dataset_tab = st.tabs(["Label", "Dataset"])

with label_tab:
    show_data = show_data_from_df("Data/RealData/hfq/600570.csv")
    chart = draw_chart(show_data)
    st_pyecharts(chart, height="200%", width="100%")

    trade_result = st.radio(label="操作", options=["买", "卖", "保持"])

    next_button = st.button("next day")
    if next_button:
        with open("Data/LabelData/total_dataset.tsv", "a") as f:
            save_data = []
            save_data.append("600570")
            save_data.append(show_data["times"][0])
            save_data.append(show_data["times"][-1])
            save_data.append(trade_result)
            line = "\t".join(save_data)
            f.write(f"{line}\n")

        st.success("保存成功", icon="✅")

with dataset_tab:
    rank_texts_list = []
    with open("Data/LabelData/total_dataset.tsv", "r", encoding="utf8") as f:
        for i, line in enumerate(f.readlines()):
            texts = line.strip().split("\t")
            rank_texts_list.append(texts)
    df = pd.DataFrame(
        np.array(rank_texts_list),
        columns=(["code", "start_time", "end_time", "trade_result"]),
    )
    st.dataframe(df,use_container_width=True)
