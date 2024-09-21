"""
Description:
Author: adolf
Date: 2022-07-23 16:04:07
LastEditTime: 2022-08-18 23:25:46
LastEditors: adolf
"""

import json
import os

from loguru import logger
from tqdm.auto import tqdm

from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict

# import akshare as ak
# from pprint import pprint
from GetBaseData.thirdpart.stock_board_industry_em import (
    stock_board_industry_hist_em,
    stock_board_industry_name_em,
)

logger.info("开始获取股票板块数据")

# stock_board_concept_name_em_df = ak.stock_board_concept_name_em()
# print(stock_board_concept_name_em_df)

# board_name_mapping = stock_board_concept_name_em_df.set_index(['板块名称'])['板块代码'].to_dict()
# pprint(board_name_mapping)

# with open("Data/BoardData/ALL_BOARD_NAME.json", "w") as all_market_code:
#     json.dump(board_name_mapping, all_market_code, ensure_ascii=False)

# stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
stock_board_industry_name_em_df = stock_board_industry_name_em()
# print(stock_board_industry_name_em_df)

industry_board_name_mapping = stock_board_industry_name_em_df.set_index(["板块名称"])[
    "板块代码"
].to_dict()
# pprint(industry_board_name_mapping)

with open("Data/BoardData/ALL_INDUSTRY_BOARD.json", "w") as all_market_code:
    json.dump(industry_board_name_mapping, all_market_code, ensure_ascii=False)

save_path = "Data/BoardData/industry_origin/"
if not os.path.exists(save_path):
    os.mkdir(save_path)

for key, value in tqdm(industry_board_name_mapping.items()):
    # print(key,value)
    try:
        # stock_board_industry_hist_em_df = ak.stock_board_industry_hist_em(
        #     symbol=key, start_date="19900101", end_date="20991231", adjust="")
        stock_board_industry_hist_em_df = stock_board_industry_hist_em(
            symbol=key, start_date="19900101", end_date="20991231", adjust=""
        )

        stock_board_industry_hist_em_df.rename(
            columns=ch_eng_mapping_dict, inplace=True
        )
        # print(stock_board_industry_hist_em_df)

        stock_board_industry_hist_em_df.to_csv(save_path + f"{key}.csv", index=False)

    except Exception as e:
        logger.error(e)
        logger.error(key)
