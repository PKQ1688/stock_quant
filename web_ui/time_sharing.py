"""
@Author       : adolf adolf1321794021@gmail.com
@Date         : 2023-06-08 23:07:44
@LastEditors  : adolf
@LastEditTime : 2023-06-10 16:04:20
@FilePath     : /stock_quant/web_ui/time_sharing.py
@Description  : 
"""
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import baostock as bs



def get_index_data(code="sh.000001"):
    rs = bs.query_history_k_data_plus(
        code=code,
        fields="date,code,close",
        start_date="2013-01-01",
        end_date="2023-06-10",
        frequency="d",
        adjustflag="3",
    )
    # 打印结果集
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result_df = pd.DataFrame(data_list, columns=rs.fields)
    return result_df

if "df_sh" not in st.session_state:
    bs.login()

    st.session_state["df_sh"] = get_index_data(code="sh.000001")
    st.session_state["df_sz"] = get_index_data(code="sz.399001")
    st.session_state["df_cr"] = get_index_data(code="sz.399006")

    bs.logout()

# st.dataframe(df_sh)

x_data_sz = st.session_state["df_sh"]["date"].tolist()  # 日期
y_data_sz = st.session_state["df_sz"]["close"].tolist()
y_data_sh = st.session_state["df_sh"]["close"].tolist()
y_data_cr = st.session_state["df_cr"]["close"].tolist()  # 收盘价


def three_inidexs():
    st.title("指数历史行情")

    options = {
        "title": {"text": "三大指数走势"},
        "legend": {"data": ["上证指数", "深证指数", "创业板指数"]},
        "xAxis": {
            "type": "category",
            "data": x_data_sz,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "上证指数",
                "type": "line",
                "data": y_data_sh,
            },
            {
                "name": "深证指数",
                "type": "line",
                "data": y_data_sz,
            },
            {
                "name": "创业板指数",
                "type": "line",
                "data": y_data_cr,
            },
        ],
    }

    st_echarts(options=options, height="600px")
