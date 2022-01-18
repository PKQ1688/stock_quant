# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/18 22:08
# @Author  : Adolf
# @File    : BaseInfoStockMonitor.py
# @Function:
import akshare as ak
import json
from Utils.info_push import post_msg_to_dingtalk
from PrivacyConfig.dingtalk import dingtalk_config, code_name_list


def get_stock_name_mapping():
    with open(file="Data/RealData/ALL_MARKET_CODE.json", encoding="utf-8", mode="r") as f:
        _market_code_dict = json.load(f)
        _market_code_dict = dict(zip(_market_code_dict.values(), _market_code_dict.keys()))

    return _market_code_dict


# market_code_dict = get_stock_name_mapping()

# 获取全市场股票的最近价
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()


def get_stock_individual_info(code_name):
    # code_id = market_code_dict[code_name]
    stock_spot = stock_zh_a_spot_em_df[stock_zh_a_spot_em_df["名称"] == code_name]
    return stock_spot.to_dict('list')  # ["最新价"][0]


def push_one_stock_info(_code_name):
    res = get_stock_individual_info(_code_name)
    message = "名称:{},最新价:{},涨跌幅:{}%".format(_code_name, res["最新价"][0], res["涨跌幅"][0])
    print(message)
    post_msg_to_dingtalk(msg=message, title=dingtalk_config["title"], token=dingtalk_config["token"])


for code_name in code_name_list:
    push_one_stock_info(_code_name=code_name)
