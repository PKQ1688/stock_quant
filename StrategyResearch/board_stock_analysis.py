"""
Description:
Author: adolf
Date: 2022-07-26 22:52:23
LastEditTime: 2022-07-26 23:11:39
LastEditors: adolf
"""

import akshare as ak
import pandas as pd
from loguru import logger

from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 500)

stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol="通用设备")

stock_board_industry_cons_em_df.rename(columns=ch_eng_mapping_dict, inplace=True)
reserve_list = ["code", "name", "pctChg", "price", "pre_close", "turn"]
stock_board_industry_cons_em_df = stock_board_industry_cons_em_df[reserve_list]

stock_board_industry_cons_em_df["pct"] = (
    stock_board_industry_cons_em_df["price"]
    / stock_board_industry_cons_em_df["pre_close"]
    - 1
) * 100
stock_board_industry_cons_em_df.sort_values(by=["pct"], ascending=False, inplace=True)
stock_board_industry_cons_em_df = stock_board_industry_cons_em_df.round(2)

logger.info(stock_board_industry_cons_em_df)
