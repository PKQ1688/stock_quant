# @Project : stock_quant
# @Date    : 2021/11/30 23:07
# @Author  : Adolf
# @File    : get_dc_data.py
# @Function:

import json
import shutil
import time
from pathlib import Path

import akshare as ak
import pandas as pd
import ray
from loguru import logger
from tqdm.auto import tqdm

from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict

pd.set_option("expand_frame_repr", False)

logger.info("开始获取股票日线数据")

only_hfq = True
all_data = False
# 获取实时行情数据
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
stock_zh_a_spot_em_df.rename(columns=ch_eng_mapping_dict, inplace=True)
stock_zh_a_spot_em_df.sort_values(
    by="TMC", ascending=False, inplace=True
)  # 按照市值排序

if not all_data:
    stock_zh_a_spot_em_df = stock_zh_a_spot_em_df.head(500)

code_list = stock_zh_a_spot_em_df.code.to_list()

code_name_mapping = stock_zh_a_spot_em_df.set_index(["code"])["name"].to_dict()
# breakpoint()

data_path = Path("Data")
real_data_path = Path("Data/RealData")

if not data_path.exists():
    data_path.mkdir()

if not real_data_path.exists():
    real_data_path.mkdir()

with real_data_path.joinpath("ALL_MARKET_CODE.json").open("w") as all_market_code:
    json.dump(code_name_mapping, all_market_code, ensure_ascii=False)

ray.init()

error_code_list = []

hfq_path = Path("Data/RealData/hfq/")
if hfq_path.exists():
    shutil.rmtree(hfq_path)
hfq_path.mkdir()


if not only_hfq:
    qfq_path = Path("Data/RealData/qfq/")
    if qfq_path.exists():
        shutil.rmtree(qfq_path)

    origin_path = Path("Data/RealData/origin/")
    if origin_path.exists():
        shutil.rmtree(origin_path)

    qfq_path.mkdir()
    origin_path.mkdir()


@ray.remote
def get_one_stock_data(code):
    try:
        # 获取后复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq")
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        # stock_zh_a_hist_df["industry"] = get_stock_board_df(code)
        stock_zh_a_hist_df.to_csv(hfq_path.joinpath(code + ".csv"), index=False)

        if not only_hfq:
            # 获取前复权数据
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="qfq")
            stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
            # if len(stock_zh_a_hist_df) < 120:
            #     return 0
            stock_zh_a_hist_df["code"] = code
            stock_zh_a_hist_df["name"] = code_name_mapping[code]
            stock_zh_a_hist_df.to_csv(qfq_path.joinpath(code + ".csv"), index=False)

            # 获取原始不复权数据
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code)
            stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
            # if len(stock_zh_a_hist_df) < 120:
            #     return 0
            stock_zh_a_hist_df["code"] = code
            stock_zh_a_hist_df["name"] = code_name_mapping[code]
            # stock_zh_a_hist_df["industry"] = get_stock_board_df(code)
            stock_zh_a_hist_df.to_csv(origin_path.joinpath(code + ".csv"), index=False)
            # pbar.update(1)

        return 0
    except Exception as e:
        logger.error(code)
        logger.error(e)
        error_code_list.append(code)
        # pbar.update(1)


start_time = time.time()
futures = [get_one_stock_data.remote(code) for code in code_list]


# ray.get(futures)
# for code in code_list:
# get_one_stock_data(code)
def to_iterator(obj_ids):
    while obj_ids:
        done, obj_ids = ray.wait(obj_ids)
        yield ray.get(done[0])


for _ in tqdm(to_iterator(futures), total=len(code_list)):
    pass

print(
    f"本次获取了{len(code_list)}只股票的数据,共用时间为{time.time() - start_time:.2f}"
)
# pbar.close()
print("date", time.strftime("%Y-%m-%d"))
print("=" * 20)
