'''
Description:  
Author: adolf
Date: 2022-07-24 14:09:47
LastEditTime: 2022-07-26 23:10:51
LastEditors: adolf
'''
import os
import json
from pprint import pprint
import pandas as pd
from finta import TA
from loguru import logger
# from Utils.base_utils import logger
os.environ["LOGURU_LEVEL"] = "INFO"
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_rows', 100)

board_data_path = "Data/BoardData/"

with open(board_data_path + "ALL_INDUSTRY_BOARD.json", 'r') as f:
    board_dict = json.load(f)

# pprint(board_dict)

board_list = board_dict.keys()
# board_mom_dict = {}
mom_list = []
mom_sma_list = []
for one_board in board_list:
    # print(one_board)
    df = pd.read_csv(board_data_path +
                     "industry_origin/{}.csv".format(one_board))
    df = df[["date", "open", "close", "high", "low", "volume"]]
    # print(df)

    df["mom"] = TA.MOM(df, period=20)
    # print(df)
    df["mom_sma"] = TA.SMA(df, period=10, column="mom")
    # print(df)
    mom_list.append(round(df.mom.tail(1).item(), 3))
    mom_sma_list.append(round(df.mom_sma.tail(1).item(), 3))
    # board_mom_dict[one_board] = {}
    # board_mom_dict[one_board]['mom'] = round(df.mom.tail(1).item(),3)
    # board_mom_dict[one_board]['mom_sma'] = round(df.mom_sma.tail(1).item(),3)
    # break

# pprint(board_mom_dict)
board_mom_dict = {
    "board": board_list,
    "mom": mom_list,
    "mom_sma": mom_sma_list
}
board_mom_df = pd.DataFrame.from_dict(board_mom_dict)
board_mom_df['code'] = board_mom_df['board'].apply(lambda x: board_dict[x])
board_mom_df.sort_values(by=['mom_sma','mom'],ascending=False,inplace=True)
logger.debug(board_mom_df)