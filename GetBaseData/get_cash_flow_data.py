"""
Description:
Author: adolf
Date: 2022-07-10 15:46:40
LastEditTime: 2022-09-23 00:01:35
LastEditors: adolf
"""

import json
import os

import akshare as ak

# from pprint import pprint
import pandas as pd
from loguru import logger

logger.info("开始获取股票现金流数据")

import time

import ray
from tqdm.auto import tqdm

ray.init()


@ray.remote
def get_one_stock_cash_data(code):
    try:
        if not os.path.exists("Data/CashFlow/"):
            os.mkdir("Data/CashFlow/")

        csv_path = f"Data/CashFlow/{code}.csv"
        # print(code[0])
        # exit()
        if code[0] == "6":
            market = "sh"
        else:
            market = "sz"
        now = ak.stock_individual_fund_flow(stock=code, market=market)
        if os.path.exists(csv_path):
            # print(code)
            origin = pd.read_csv(csv_path)
            now = pd.merge(origin, now, how="inner")
        now.to_csv(csv_path, index=False)
    except Exception as e:
        logger.error(e)
        logger.error(code)
        # error_code_list.append(code)


# code = 300389
# test_df = ak.stock_individual_fund_flow(stock=code,market="sz")
# exit()

with open("Data/RealData/ALL_MARKET_CODE.json") as all_market_code:
    market_code_dict = json.load(all_market_code)

code_list = list(market_code_dict.keys())

start = time.time()
# error_code_list = []
# for code in tqdm(code_list):
# get_count = get_one_stock_cash_data(code,error_code_list)

# error_stock_list = [market_code_dict[code] for code in error_code_list]
# print(error_stock_list)
# print(len(error_code_list))


futures = [get_one_stock_cash_data.remote(code) for code in code_list]


def to_iterator(obj_ids):
    while obj_ids:
        done, obj_ids = ray.wait(obj_ids)
        yield ray.get(done[0])


for x in tqdm(to_iterator(futures), total=len(code_list)):
    pass

print("use data:", time.time() - start)
