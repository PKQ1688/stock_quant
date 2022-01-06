#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant 
# @Date    : 2022/1/6 16:55
# @Author  : Adolf
# @File    : base_kline.py
from typing import List, Sequence, Union

from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline, Line, Bar, Grid

from GetBaseData.hanle_data_show import get_show_data


def draw_chart(input_data):
    kline = Kline()
    kline.add_xaxis(xaxis_data=input_data["times"])
    kline.add_yaxis(
        series_name="",
        y_axis=data["datas"],
    )

    kline.render(path="ShowHtml/CandleChart.html")


if __name__ == '__main__':
    data = get_show_data("Data/RealData/hfq/600570.csv")
    draw_chart(data)
