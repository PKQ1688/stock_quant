'''
Description:  
Author: adolf
Date: 2022-07-26 23:45:09
LastEditTime: 2022-07-26 23:54:14
LastEditors: adolf
'''
import akshare as ak

# 问财热度排行
stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date="20220726")
print(stock_hot_rank_wc_df)

# 东财热度排行
stock_hot_rank_em_df = ak.stock_hot_rank_em()
print(stock_hot_rank_em_df)

# 淘股吧热度排行
stock_hot_tgb_df = ak.stock_hot_tgb()
print(stock_hot_tgb_df)