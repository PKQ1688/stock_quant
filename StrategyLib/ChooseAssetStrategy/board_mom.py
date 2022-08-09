'''
Description: 
Author: adolf
Date: 2022-08-09 23:11:43
LastEditTime: 2022-08-09 23:14:54
LastEditors: adolf
'''
from BackTrader.market_choose import MarketChoose

class BoardMoMStrategy(MarketChoose):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def cal_one_data(self):
        pass


if __name__ == "__main__":
    board_mom_strategy = BoardMoMStrategy(LOG_LEVEL="INFO")