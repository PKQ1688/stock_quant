#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant
# @Date    : 2022/1/6 16:55
# @Author  : Adolf
# @File    : base_kline.py
from tkinter.messagebox import NO
from typing import List, Sequence, Union

from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline, Line, Bar, Grid

# from snapshot_pyppeteer import snapshot
# from pyecharts.render import make_snapshot
from pyecharts.options import InitOpts


def calculate_ma(input_data, day_count: int):
    result: List[Union[float, str]] = []

    for i in range(len(input_data["times"])):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(input_data["datas"][i - j][1])
        result.append(abs(float("%.2f" % (sum_total / day_count))))
    return result


def draw_chart(input_data, show_html_path="ShowHtml/CandleChart.html"):
    kline = Kline()
    points = []
    colors_div = {"buy": "red", "sell": "green"}
    for lable in ["buy", "sell"]:
        for i, val in enumerate(input_data[lable]):
            if val == 1:
                coord = [input_data["times"][i], input_data["datas"][i][1]]
                point = opts.MarkPointItem(coord=coord, name=lable,itemstyle_opts={"color":colors_div[lable]})
                points.append(point)

    # points.extend([opts.MarkPointItem(type_="max", name="最大值"),
    #                opts.MarkPointItem(type_="min", name="最小值")])
    
    # import pdb;pdb.set_trace()
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
        markpoint_opts=opts.MarkPointOpts(data=points),
        # markline_opts=opts.MarkLineOpts(
        #     label_opts=opts.LabelOpts(
        #         position="middle", color="blue", font_size=15
        #     ),
        #     data=split_data_part(input_data),
        #     symbol=["circle", "none"],
        # ),
    )
    # kline.set_series_opts(
    #         markarea_opts=opts.MarkAreaOpts(is_silent=True, data=split_data_part())
    #     )
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
                is_show=True, type_="inside", xaxis_index=[0, 0], range_end=100
            ),
            opts.DataZoomOpts(
                is_show=True, xaxis_index=[0, 1], pos_top="97%", range_end=100
            ),
            opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2], range_end=100),
        ],
    )

    kline_line_ma = Line()
    kline_line_ma.add_xaxis(xaxis_data=input_data["times"])
    kline_line_ma.add_yaxis(
        series_name="MA5",
        y_axis=calculate_ma(input_data=input_data, day_count=5),
        is_smooth=True,
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
        is_symbol_show=False,
    )
    kline_line_ma.add_yaxis(
        series_name="MA10",
        y_axis=calculate_ma(input_data=input_data, day_count=10),
        is_smooth=True,
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
        is_symbol_show=False,
    )
    kline_line_ma.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=1,
            split_number=3,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=True),
        ),
    )
    overlap_kline_line = kline.overlap(kline_line_ma)

    # bar_vol = Bar()
    # bar_vol.add_xaxis(xaxis_data=input_data["times"])
    # bar_vol.add_yaxis(
    #     series_name="Volumn",
    #     y_axis=input_data["vols"],
    #     xaxis_index=1,
    #     yaxis_index=1,
    #     label_opts=opts.LabelOpts(is_show=False),
    #     # 根据 echarts demo 的原版是这么写的
    #     # itemstyle_opts=opts.ItemStyleOpts(
    #     #     color=JsCode(
    #     #         """
    #     #     function(params) {
    #     #         var colorList;
    #     #         if (input_data.datas[params.dataIndex][1]>input_data.datas[params.dataIndex][0]) {
    #     #           colorList = '#ef232a';
    #     #         } else {
    #     #           colorList = '#14b143';
    #     #         }
    #     #         return colorList;
    #     #     }
    #     #     """)
    #     # )
    #     # 改进后在 grid 中 add_js_funcs 后变成如下
    #     itemstyle_opts=opts.ItemStyleOpts(
    #         color=JsCode(
    #             """
    #             function(params) {
    #                 var colorList;
    #                 if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
    #                     colorList = '#ef232a';
    #                 } else {
    #                     colorList = '#14b143';
    #                 }
    #                 return colorList;
    #             }
    #             """
    #         )
    #     ),
    # )
    # bar_vol.set_global_opts(
    #     xaxis_opts=opts.AxisOpts(
    #         type_="category",
    #         grid_index=1,
    #         axislabel_opts=opts.LabelOpts(is_show=False),
    #     ),
    #     legend_opts=opts.LegendOpts(is_show=False),
    # )

    # 成交量图
    bar_vol = Bar()
    bar_vol.add_xaxis(input_data["times"])
    bar_vol.add_yaxis(
        series_name="Volume",
        y_axis=input_data["vols"],
        bar_width="60%",
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
                    function(params) {
                        var colorList;
                        if (params.data >= 0) {
                          colorList = '#ef232a';
                        } else {
                          colorList = '#14b143';
                        }
                        return colorList;
                    }
                """
            )
        ),
    )
    bar_vol.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=True, font_size=8, color="#9b9da9"),
            is_show=False,
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            axislabel_opts=opts.LabelOpts(
                color="#c7c7c7", font_size=8, position="inside", is_show=False
            ),
            is_show=False,
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )

    # macd图
    bar_macd = Bar()
    bar_macd.add_xaxis(xaxis_data=input_data["times"])
    bar_macd.add_yaxis(
        series_name="MACD",
        y_axis=input_data["macds"],
        xaxis_index=2,
        yaxis_index=2,
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
                    function(params) {
                        var colorList;
                        if (params.data >= 0) {
                          colorList = '#ef232a';
                        } else {
                          colorList = '#14b143';
                        }
                        return colorList;
                    }
                """
            )
        ),
    )
    bar_macd.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=2,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=2,
            split_number=4,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=True),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )

    line_macd = Line()
    line_macd.add_xaxis(xaxis_data=input_data["times"])
    line_macd.add_yaxis(
        series_name="DIF",
        y_axis=input_data["difs"],
        xaxis_index=2,
        yaxis_index=2,
        label_opts=opts.LabelOpts(is_show=False),
        is_symbol_show=False,
    )
    line_macd.add_yaxis(
        series_name="DEA",
        y_axis=input_data["deas"],
        xaxis_index=2,
        yaxis_index=2,
        label_opts=opts.LabelOpts(is_show=False),
        is_symbol_show=False,
    )
    line_macd.set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    overlap_macd_line = bar_macd.overlap(line_macd)
    ops = InitOpts(width="100%", height="800px")
    grid_chart = Grid(init_opts=ops)
    # grid_chart = Grid()
    grid_chart.add_js_funcs("var barData = {}".format(input_data["datas"]))

    grid_chart.add(
        overlap_kline_line,
        # grid_opts=grid0_opts,
        grid_opts=opts.GridOpts(pos_left="3%", pos_right="1%", height="60%"),
    )

    # # Volumn 柱状图
    grid_chart.add(
        bar_vol,
        # grid_opts=grid1_opts
        grid_opts=opts.GridOpts(
            pos_left="3%", pos_right="1%", pos_top="71%", height="10%"
        ),
    )

    # # MACD DIFS DEAS
    grid_chart.add(
        overlap_macd_line,
        # grid_opts=grid2_opts,
        grid_opts=opts.GridOpts(
            pos_left="3%", pos_right="1%", pos_top="82%", height="14%"
        ),
    )

    # grid_chart.render(path="ShowHtml/CandleChart.html")

    if show_html_path is not None:
        grid_chart.render(path=show_html_path, height="600%", width="100%")

    return grid_chart
    # if show_render:
    #     grid_chart.render()
    #     make_snapshot(snapshot, grid_chart.render(), "bar.png")


if __name__ == "__main__":
    from GetBaseData.hanle_data_show import show_data_from_df

    show_data = show_data_from_df("Data/RealData/hfq/600570.csv")
    draw_chart(show_data, show_html_path="ShowHtml/CandleChartv2.html")
