"""
 Author       : adolf
 Date         : 2023-02-06 23:17:11
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-02-06 23:54:00
 FilePath     : /stock_quant/StrategyLib/AutomaticInvestmentPlan/result_show.py
"""
import pandas as pd

from StrategyLib.AutomaticInvestmentPlan.stable_dog import get_AI_plan_result
import streamlit as st
from datetime import datetime


def getDays(day1, day2):
    # 获取需要计算的时间戳
    d1 = datetime.strptime(day1, '%Y-%m-%d')
    d2 = datetime.strptime(day2, '%Y-%m-%d')
    interval = d2 - d1  # 两日期差距
    return interval.days


st.subheader("Stable unstop ")
code = st.sidebar.text_input("code", value="sz.399006")
gap_days = st.sidebar.text_input("interval", value=1)
first_buy_day = st.sidebar.text_input("start", value="2019-01-02")
end_buy_day = st.sidebar.text_input("end", value="2023-02-06")

want_rate = st.sidebar.text_input("target", value=1.1)
if_intelli = st.sidebar.text_input("if_intelli", value="yes")
threshold = st.sidebar.text_input("threshold", value=100000)

records = []
total_earned = 0
start = first_buy_day
while start < end_buy_day:
    res, _ = get_AI_plan_result(code=code,
                                gap_days=int(gap_days),
                                first_buy_day=start,
                                want_rate=float(want_rate),
                                if_intelli=if_intelli == "yes",
                                threshold=int(threshold))
    if len(res) == 0:
        break
    earned = res.loc[len(res) - 1, 'account'] - res.loc[len(res) - 1, 'put_in']
    total_earned += earned
    end = res.loc[len(res) - 1, 'date']
    records.append([start, end,res.loc[len(res) - 1, 'put_in'], earned, total_earned])
    start = end
    print(records[-1])

records = pd.DataFrame(records, columns=['start', 'end','put_in', 'earned', 'total_earned'])
print("总收益为%d" % total_earned)
natual_day = getDays(records.loc[0, 'start'], records.loc[len(records) - 1, 'end'])
# 股票曲线图
stock_data = pd.read_csv(f"Data/RealData/Baostock/day/{code}.csv")
stock_data = stock_data[stock_data["tradestatus"] == 1]
stock_data = stock_data[["date", "code", "open", "high", "low", "close", "volume"]]
stock_data = stock_data[(stock_data["date"] >= first_buy_day) & (stock_data["date"] <= end_buy_day)]

print("records:")
print(records)
stock_data.reset_index(drop=True, inplace=True)
st.text(
    f"自然日天数:{natual_day}，总收益:{total_earned} ,标的涨跌幅:{stock_data.loc[len(stock_data) - 1, 'close'] / stock_data.loc[0, 'open']}")
st.dataframe(records, width=900)
st.line_chart(records, y="total_earned")
st.line_chart(stock_data, y="close", x='date')
