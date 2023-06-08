import streamlit as st
from streamlit_echarts import st_echarts
import baostock as bs
import pandas as pd

lg = bs.login()
# 获取上证指数当天的行情数据

rs = bs.query_history_k_data_plus("sh.000001",
                                  "date,code,open,high,low,close,volume",
                                  start_date='2023-06-07',
                                  end_date='2023-06-08',
                                  frequency="5",
                                  adjustflag="3")

# 打印结果集
data_list = []
while rs.next():
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

print(result)
# 登出系统
bs.logout()

st.title("分时行情")

option = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)