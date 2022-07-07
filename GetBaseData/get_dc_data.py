# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2021/11/30 23:07
# @Author  : Adolf
# @File    : get_dc_data.py
# @Function:

import os.path
import time

import ray
# import socket
import pandas as pd
import akshare as ak
from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict
import shutil
from tqdm.auto import tqdm

import json

pd.set_option("expand_frame_repr", False)
# socket.gethostbyname("")
# 获取实时行情数据
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
stock_zh_a_spot_em_df.rename(columns=ch_eng_mapping_dict, inplace=True)
code_list = stock_zh_a_spot_em_df.code.to_list()

code_name_mapping = stock_zh_a_spot_em_df.set_index(['code'])['name'].to_dict()
with open("Data/RealData/ALL_MARKET_CODE.json", "w") as all_market_code:
    json.dump(code_name_mapping, all_market_code)

ray.init()

error_code_list = []

qfq_path = "Data/RealData/qfq/"
hfq_path = "Data/RealData/hfq/"
origin_path = "Data/RealData/origin/"

if os.path.exists(qfq_path):
    shutil.rmtree(qfq_path)
if os.path.exists(hfq_path):
    shutil.rmtree(hfq_path)
if os.path.exists(origin_path):
    shutil.rmtree(origin_path)

os.mkdir(qfq_path)
os.mkdir(hfq_path)
os.mkdir(origin_path)

# pbar = tqdm(total=len(code_list))


@ray.remote
def get_one_stock_data(code):
    try:
        # 获取前复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="qfq")
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        stock_zh_a_hist_df.to_csv(os.path.join(qfq_path, code + ".csv"), index=False)

        # 获取后复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq")
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        # stock_zh_a_hist_df["industry"] = get_stock_board_df(code)
        stock_zh_a_hist_df.to_csv(os.path.join(hfq_path, code + ".csv"), index=False)

        # 获取原始不复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code)
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        # stock_zh_a_hist_df["industry"] = get_stock_board_df(code)
        stock_zh_a_hist_df.to_csv(os.path.join(origin_path, code + ".csv"), index=False)
        # pbar.update(1)

        return 0
    except Exception as e:
        print(code)
        print(e)
        error_code_list.append(code)
        # pbar.update(1)


start_time = time.time
futures = [get_one_stock_data.remote(code) for code in code_list]


# ray.get(futures)
# for code in code_list:
# get_one_stock_data(code)
def to_iterator(obj_ids):
    while obj_ids:
        done, obj_ids = ray.wait(obj_ids)
        yield ray.get(done[0])


for x in tqdm(to_iterator(futures), total=len(code_list)):
    pass

print('本次获取了{}只股票的数据，共用时间为{}'.format(len(code_list, time.time - start_time)))
# pbar.close()
print("date", time.strftime("%Y-%m-%d"))
print("=" * 20)
