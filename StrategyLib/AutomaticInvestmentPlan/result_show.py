"""
 Author       : adolf
 Date         : 2023-02-06 23:17:11
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-02-06 23:54:00
 FilePath     : /stock_quant/StrategyLib/AutomaticInvestmentPlan/result_show.py
"""
from StrategyLib.AutomaticInvestmentPlan.stable_dog import get_AI_plan_result
import streamlit as st
import matplotlib.pyplot as plt

st.title("稳狗策略")

code = st.sidebar.text_input("股票代码", value="sh.600000")
gap_days = st.sidebar.text_input("间隔天数", value=3)
first_buy_day = st.sidebar.text_input("首次买入日期", value="2019-01-02")
want_rate = st.sidebar.text_input("目标收益率", value=1.1)

res = get_AI_plan_result(code=code, 
                         gap_days=int(gap_days), 
                         first_buy_day=first_buy_day, 
                         want_rate=float(want_rate))
res.drop(["buy_index"], axis=1, inplace=True)
st.dataframe(res)

chart_data = res[["rate"]].apply(lambda x: (x - 1)*100)
st.line_chart(chart_data,y="rate")