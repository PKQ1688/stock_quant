'''
Description: 
Author: adolf
Date: 2022-08-13 21:45:35
LastEditTime: 2022-08-13 21:49:09
LastEditors: adolf
'''
import sys
from loguru import logger

class CoreTradeLogic:
    def __init__(self) -> None:
        self.trade_rate = 1.5 / 1000
        
        self.logger = logger
        self.logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
        self.logger.add(sys.stderr, level=self.config.LOG_LEVEL)  # 添加一个终端输出的内容
        # logger.add("some_file.log", enqueue=True)  #添加一个文件输出的内容


    @staticmethod
    def init_one_transaction_record(asset_name):
        return {
            "pos_asset": asset_name,
            "buy_date": "",
            "buy_price": 1,
            "sell_date": "",
            "sell_price": 1,
            "holding_time": 0
        }

    def get_