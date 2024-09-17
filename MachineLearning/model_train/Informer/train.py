# -*- coding: UTF-8 -*-
"""
@Project ：stock_quant
@File    ：train.py
@Author  ：adolf
@Date    ：2023/4/5 21:41
"""

from datasets import load_dataset

dataset = load_dataset("monash_tsf", "traffic_hourly")
print(dataset)
