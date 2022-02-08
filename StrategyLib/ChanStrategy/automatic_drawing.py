# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/5 17:22
# @Author  : Adolf
# @File    : automatic_drawing.py
# @Function:
import streamlit as st
import akshare as ak
import os
import pandas as pd
from StrategyLib.ChanStrategy.BasicChan.basic_tools import CZSC, RawBar
from streamlit_echarts import st_pyecharts
import streamlit.components.v1 as components

symbol = st.sidebar.text_input('stock code', '000001')
period = st.sidebar.selectbox('time period', ('daily', 'weekly', 'monthly', '1min', '5min', '15min', '30min', '60min'))
adjust = st.sidebar.selectbox('time period', ('qfq', 'hfq', 'origin'))

start_date = None
end_date = None

if period in ['daily', 'weekly', 'monthly']:
    start_date = st.sidebar.text_input('start time', '20170301')
    end_date = st.sidebar.text_input('end time', '20210907')

# 'You selected:', option

st.title('股票数据展示')
st.write("下面是表格")

if period in ['daily', 'weekly', 'monthly']:
    df = ak.stock_zh_a_hist(symbol=symbol,
                            period=period,  # choice of {'daily', 'weekly', 'monthly'}
                            start_date=start_date,
                            end_date=end_date,
                            adjust=adjust)

    bars = [RawBar(symbol=symbol, id=i, freq=period, open=row['开盘'], dt=row['日期'],
                   close=row['收盘'], high=row['最高'], low=row['最低'], vol=row['成交量'],
                   amount=row['成交额'])
            for i, row in df.iterrows()]

elif period in ['1min', '5min', '15min', '30min', '60min']:
    df = ak.stock_zh_a_hist_min_em(symbol=symbol,
                                   period=period.replace("min", ""),
                                   adjust=adjust)

    bars = [RawBar(symbol=symbol, id=i, freq=period, open=row['开盘'], dt=row['时间'],
                   close=row['收盘'], high=row['最高'], low=row['最低'], vol=row['成交量'],
                   amount=row['成交额'])
            for i, row in df.iterrows()]

else:
    raise ValueError

print(df)


ka = CZSC(bars)
file_html = 'ShowHtml/czsc_render.html'
# chart = ka.to_echarts(width="1200px", height='600px')
chart = ka.to_echarts()
st_pyecharts(chart, height="1200px", width="600px")
# chart.render(file_html)
# assert os.path.exists(file_html)
# st.write(df)
# components.html(chart, width=1200, height=600)
