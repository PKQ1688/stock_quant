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
from StrategyLib.ChanStrategy.BasicChan.basic_tools import CZSC, RawBar, get_zs_seq
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


# cur_path = os.path.split(os.path.realpath(__file__))[0]

def read_read_daily():
    file_kline = "Data/RealData/origin/000538.csv"
    kline = pd.read_csv(file_kline, encoding="utf-8")
    kline = kline[-2000:]
    kline.reset_index(drop=True, inplace=True)
    # print(kline)

    bars = [RawBar(symbol=row['name'], id=i, freq=Freq.D, open=row['open'], dt=row['date'],
                   close=row['close'], high=row['high'], low=row['low'], vol=row['volume'],
                   amount=row['amount'])
            for i, row in kline.iterrows()]

    # print(bars[0])
    return bars


def test_kline_pro():
    # file_kline = os.path.join(cur_path, "data/000001.SH_D.csv")
    bars = read_read_daily()
    ka = CZSC(bars)
    # ka.open_in_browser()
    file_html = 'ShowHtml/czsc_render.html'
    chart = ka.to_echarts(width="1200px", height='600px')
    chart.render(file_html)
    assert os.path.exists(file_html)
    # os.remove(file_html)


# test_kline_pro()

def test_get_zs_seq():
    bars = read_read_daily()
    c = CZSC(bars)
    zs_seq = get_zs_seq(c.bi_list)
    # assert len(zs_seq) == 7
    # assert len(zs_seq[-1].bis) == 20
    # print(zs_seq)
    for one_zs in zs_seq:
        print(one_zs)


test_get_zs_seq()
