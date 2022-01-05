# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/4 21:54
# @Author  : Adolf
# @File    : RUMI_config.py
# @Function:
rumi_config = {
    "log_level": "INFO",
    "code_name": "600570",
    "start_stamp": "2005-01-01",
    "end_stamp": "2020-12-31",
    "strategy_params": {
        "sma_length": [5, 10, 20, 30],
        "ema_length": [10, 20, 30, 60],
        "aos_length": [5, 10, 20, 30, 60],
    }
}
