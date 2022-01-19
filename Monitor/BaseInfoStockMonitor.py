# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/18 22:08
# @Author  : Adolf
# @File    : BaseInfoStockMonitor.py
# @Function:
import akshare as ak
import json
import datetime

from Utils.info_push import post_msg_to_dingtalk
from PrivacyConfig.dingtalk import dingtalk_config, code_name_list


# 判断是否是交易时间
def pd_ztjytime():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_datetime = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') + ' 11:30:01', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') + ' 13:00:00', '%Y-%m-%d %H:%M:%S')
    delta1 = (now_datetime - d1).total_seconds()
    delta2 = (d2 - now_datetime).total_seconds()
    if delta1 > 0 and delta2 > 0:  # 在暂停交易的时间内
        return False  # 不在暂停的交易时间范围内，返回 False
    else:
        return True  # 在暂停的交易时间范围内，返回 True


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
