'''
Description:  
Author: adolf
Date: 2022-07-26 23:45:09
LastEditTime: 2022-07-31 21:29:19
LastEditors: adolf
'''
import akshare as ak
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# 问财热度排行
stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date="20220726")
print(stock_hot_rank_wc_df)

# 东财热度排行
stock_hot_rank_em_df = ak.stock_hot_rank_em()
print(stock_hot_rank_em_df)

# 淘股吧热度排行
stock_hot_tgb_df = ak.stock_hot_tgb()
print(stock_hot_tgb_df)

# 雪球讨论热度榜
new_hot = ak.stock_hot_tweet_xq(symbol="本周新增")
new_hot['new_hot_rank'] = new_hot.index
# print(new_hot[:100])

# old_hot = ak.stock_hot_tweet_xq(symbol="最热门")
# old_hot['old_hot_rank'] = old_hot.index
# print(old_hot[:100])

# hot_df = pd.merge(new_hot, old_hot)
# hot_df['diff'] = hot_df['new_hot_rank'] - hot_df['old_hot_rank']
# # hot_df.sort_values(by='diff', ascending=False, inplace=True)
# hot_df = hot_df.loc[hot_df.new_hot_rank < 2000]
# print(hot_df[:100])

