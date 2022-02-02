# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/2 23:13
# @Author  : Adolf
# @File    : test_plot.py
# @Function:
import os
import pandas as pd
import random
import Utils.ShowKline.chan_plot as chan_plot
from StrategyLib.ChanStrategy.BasicChan.basic_tools import CZSC, RawBar
from StrategyLib.ChanStrategy.BasicChan.basic_enum import Freq


def test_heat_map():
    data = [{"x": "{}hour".format(i), "y": "{}day".format(j), "heat": random.randint(0, 50)}
            for i in range(24) for j in range(7)]
    x_label = ["{}hour".format(i) for i in range(24)]
    y_label = ["{}day".format(i) for i in range(7)]
    hm = chan_plot.heat_map(data, x_label=x_label, y_label=y_label)
    file_html = 'ShowHtml/render.html'
    hm.render(file_html)
    assert os.path.exists(file_html)
    os.remove(file_html)


test_heat_map()

cur_path = os.path.split(os.path.realpath(__file__))[0]


def test_kline_pro():
    file_kline = os.path.join(cur_path, "data/000001.SH_D.csv")
    kline = pd.read_csv(file_kline, encoding="utf-8")
    bars = [RawBar(symbol=row['symbol'], id=i, freq=Freq.D, open=row['open'], dt=row['dt'],
                   close=row['close'], high=row['high'], low=row['low'], vol=row['vol'])
            for i, row in kline.iterrows()]
    ka = CZSC(bars)
    # ka.open_in_browser()
    file_html = 'czsc_render.html'
    chart = ka.to_echarts()
    chart.render(file_html)
    assert os.path.exists(file_html)
    os.remove(file_html)
