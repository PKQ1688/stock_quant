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


def split_data_part(input_data) -> Sequence:
    mark_line_data = []
    idx = 0
    tag = 0
    vols = 0
    for i in range(len(input_data["times"])):
        if input_data["datas"][i][5] != 0 and tag == 0:
            idx = i
            vols = input_data["datas"][i][4]
            tag = 1
        if tag == 1:
            vols += input_data["datas"][i][4]
        if input_data["datas"][i][5] != 0 or tag == 1:
            mark_line_data.append(
                [
                    {
                        "xAxis": idx,
                        "yAxis": float("%.2f" % input_data["datas"][idx][3])
                        if input_data["datas"][idx][1] > input_data["datas"][idx][0]
                        else float("%.2f" % input_data["datas"][idx][2]),
                        "value": vols,
                    },
                    {
                        "xAxis": i,
                        "yAxis": float("%.2f" % input_data["datas"][i][3])
                        if input_data["datas"][i][1] > input_data["datas"][i][0]
                        else float("%.2f" % input_data["datas"][i][2]),
                    },
                ]
            )
            idx = i
            vols = input_data["datas"][i][4]
            tag = 2
        if tag == 2:
            vols += input_data["datas"][i][4]
        if input_data["datas"][i][5] != 0 and tag == 2:
            mark_line_data.append(
                [
                    {
                        "xAxis": idx,
                        "yAxis": float("%.2f" % input_data["datas"][idx][3])
                        if input_data["datas"][i][1] > input_data["datas"][i][0]
                        else float("%.2f" % input_data["datas"][i][2]),
                        "value": str(float("%.2f" % (vols / (i - idx + 1)))) + " M",
                    },
                    {
                        "xAxis": i,
                        "yAxis": float("%.2f" % input_data["datas"][i][3])
                        if input_data["datas"][i][1] > input_data["datas"][i][0]
                        else float("%.2f" % input_data["datas"][i][2]),
                    },
                ]
            )
            idx = i
            vols = input_data["datas"][i][4]
    return mark_line_data


def draw_chart(input_data):
    kline = Kline()
    kline.add_xaxis(xaxis_data=input_data["times"])
    kline.add_yaxis(
        series_name="",
        y_axis=input_data["datas"],
        itemstyle_opts=opts.ItemStyleOpts(
            color="#ef232a",
            color0="#14b143",
            border_color="#ef232a",
            border_color0="#14b143",
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            label_opts=opts.LabelOpts(
                position="middle", color="blue", font_size=15
            ),
            data=split_data_part(input_data),
            symbol=["circle", "none"],
        ),
    )
    kline.set_series_opts(
        markarea_opts=opts.MarkAreaOpts(is_silent=True, data=split_data_part(input_data))
    )
    kline.set_global_opts(
        title_opts=opts.TitleOpts(title="K线展示图", pos_left="0"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            is_scale=True,
            boundary_gap=False,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            split_number=20,
            min_="dataMin",
            max_="dataMax",
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100
            ),
            opts.DataZoomOpts(
                is_show=True, xaxis_index=[0, 1], pos_top="97%", range_end=100
            ),
            opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2], range_end=100),
        ],
    )

    kline.render(path="ShowHtml/CandleChart.html")


if __name__ == '__main__':
    show_data = get_show_data("Data/RealData/hfq/600570.csv")
    draw_chart(show_data)
    # print(split_data_part(show_data))
