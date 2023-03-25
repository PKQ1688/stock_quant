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
from datetime import datetime


def getDays(day1, day2):
    # 获取需要计算的时间戳
    d1 = datetime.strptime(day1, '%Y-%m-%d')
    d2 = datetime.strptime(day2, '%Y-%m-%d')
    interval = d2 - d1  # 两日期差距
    return interval.days


def auto_investment_plan():
    st.subheader("Stable ")
    code = st.sidebar.text_input("code", value="sz.399006")
    gap_days = st.sidebar.text_input("interval", value=1)
    first_buy_day = st.sidebar.text_input("start", value="2019-01-02")
    want_rate = st.sidebar.text_input("target", value=1.5)
    if_intelli = st.sidebar.text_input("if_intelli", value="yes")
    threshold = st.sidebar.text_input("threshold", value=500000)

    res, stock_data = get_AI_plan_result(code=code,
                                         gap_days=int(gap_days),
                                         first_buy_day=first_buy_day,
                                         want_rate=float(want_rate),
                                         if_intelli=if_intelli == "yes",
                                         threshold=int(threshold))
    res.drop(["buy_index"], axis=1, inplace=True)
    st.dataframe(res, width=900)
    natual_day = getDays(res.loc[0, 'date'], res.loc[len(res) - 1, 'date'])
    st.text(
        f"达成目标自然日天数:{natual_day}，投入次数/总金额:{len(res[res['put'] != 0])}/{int(res.loc[len(res) - 1, 'put_in'])}，总收益:{int(res.loc[len(res) - 1, 'account'] - res.loc[len(res) - 1, 'put_in'])}，收益率:{round(res.loc[len(res) - 1, 'rate'], 3)},标的涨跌幅:{stock_data.loc[len(stock_data) - 1, 'close'] / stock_data.loc[0, 'open']}")
    chart_data = res[["rate"]].apply(lambda x: (x - 1) * 100)
    st.line_chart(chart_data, y="rate")
    st.line_chart(res, y="put_in")
    st.line_chart(stock_data, y="close", x='date')
