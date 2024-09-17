# -*- coding: UTF-8 -*-
"""
@Project :stock_quant
@File    :show_page.py
@Author  :adolf
@Date    :2023/3/25 16:24
"""

import streamlit as st
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

# from MachineLearning.annotation_platform.buy_and_sell_signals import (
#     annotation_platform_main,
# )
from StrategyLib.AutomaticInvestmentPlan.result_show import auto_investment_plan
from StrategyLib.ChanStrategy.automatic_drawing import chan_show_main
from StrategyLib.OneAssetStrategy.macd_day import MACDdayStrategy
from web_ui.time_sharing import three_inidexs

st.set_page_config(page_title="量化炒股系统", layout="wide")


class MultiApp:
    def __init__(self):
        self.apps = []
        self.app_dict = {}

    def add_app(self, title, func):
        if title not in self.apps:
            self.apps.append(title)
            self.app_dict[title] = func

    def run(self):
        title = st.sidebar.radio(
            "选择服务类型", self.apps, format_func=lambda title: str(title)
        )
        self.app_dict[title]()


# st.set_page_config(layout="wide")  # 设置屏幕展开方式，宽屏模式布局更好


def welcome():
    # st.title("欢迎来到法域通测试页面！")
    # st.markdown("#### 合同智审")
    # st.markdown("* [测试接口文档](http://101.69.229.138:8131/docs)")

    st.title("量化策略回测系统")
    st.markdown("#### 今日大盘走势")

    options = {
        "xAxis": {
            "type": "",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "价格"},
        "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
    }
    st_echarts(options=options)


def MACD_main():
    # st.sidebar.text_input("请输入股票代码", value="000001")
    code = st.sidebar.text_input("请输入股票代码", value="sz.399006")
    start_date = st.sidebar.text_input("请输入开始日期", value="2019-01-01")
    end_date = st.sidebar.text_input("请输入结束日期", value="2021-01-01")
    # st.sidebar.selectbox("请选择策略", ["金买死卖", "60日上方"])
    options1 = st.multiselect(
        "选择macd策略", ["金买死卖", "60日上方操作", "250日上方操作"]
    )
    options2 = st.multiselect(
        "周期选择", ["5min", "30min", "60min", "日线", "周线", "月线"]
    )
    st.title("MACD")

    config = {
        "RANDOM_SEED": 42,
        "LOG_LEVEL": "INFO",
        "CODE_NAME": code,
        # "CODE_NAME": "ALL_MARKET_10",
        # "CODE_NAME": ["sh.600238",],
        # "CODE_NAME": ["sh.603806", "sh.603697", "sh.603700", "sh.600570", "sh.603809","sh.600238","sh.603069","sh.600764","sz.002044"],
        "START_STAMP": start_date,
        "END_STAMP": end_date,
        # "SHOW_DATA_PATH": "",
        # "STRATEGY_PARAMS": {}
    }
    strategy = MACDdayStrategy(config)
    strategy.run()
    stock_result = strategy.stock_result.astype(str)
    pl = strategy.pl_result.astype(str)

    # print('-----------------------------------')
    # print(pl)
    # print('-----------------------------------')
    # st.components.v1.iframe(src="demo.html", width=700, height=500)
    with open("ShowHtml/demo.html") as fp:  # 如果遇到decode错误，就加上合适的encoding
        text = fp.read()
    components.html(html=text, width=None, height=800, scrolling=False)

    st.table(stock_result)
    st.table(pl)


def SMA_main():
    st.title("SMA")


def Kline_challenge():
    st.markdown("#### 欢迎来到K线挑战！")
    st.markdown("* [K线挑战入口](http://127.0.0.1:8501/index)")

    # st.components.v1.iframe(src="demo.html", width=700, height=500)
    # with open("api/test.html") as fp:
    #     text = fp.read()
    # components.html(html=text, width=None, height=1200, scrolling=False)


app = MultiApp()
app.add_app("首页", three_inidexs)
app.add_app("MACD策略", MACD_main)
# app.add_app("均线策略", SMA_main)
app.add_app("定投策略", auto_investment_plan)
# app.add_app("K线游戏", annotation_platform_main)
app.add_app("K线游戏", Kline_challenge)
app.add_app("缠论", chan_show_main)
app.run()
