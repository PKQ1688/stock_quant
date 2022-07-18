'''
Description: 
Author: adolf
Date: 2022-07-10 15:46:40
LastEditTime: 2022-07-18 23:23:35
LastEditors: adolf
'''
import akshare as ak
# from pprint import pprint
import pandas as pd
import json
import os

from tqdm.auto import tqdm

#显示所有列
# pd.set_option('display.max_columns', None)
#显示所有行
# pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth', 100)


def get_one_stock_cash_data(code,error_code_list=[]):
    try:
        if not os.path.exists('Data/CashFlow/'):
            os.mkdir('Data/CashFlow/')

        csv_path = 'Data/CashFlow/{}.csv'.format(code)
        now = ak.stock_individual_fund_flow(stock=code)
        if os.path.exists(csv_path):
            origin = pd.read_csv(csv_path)
            now = pd.merge(origin, now, how='outer', on=['日期'])
        now.to_csv(csv_path, index=False)
    except Exception as e:
        print(e)
        print(code)
        error_code_list.append(code)

code = 300389
test_df = ak.stock_individual_fund_flow(stock=code)
exit()

with open("Data/RealData/ALL_MARKET_CODE.json", "r") as all_market_code:
    market_code_dict = json.load(all_market_code)

code_list = list(market_code_dict.keys())

error_code_list = []
for code in tqdm(code_list[1000:1100]):
    get_count = get_one_stock_cash_data(code,error_code_list)

print(error_code_list)
error_stock_list = [market_code_dict[code] for code in error_code_list]
print(error_stock_list)
print(len(error_code_list))
# print(stock_individual_fund_flow_df)
# exit()
# stock_fund_use = stock_individual_fund_flow_df[[
#     '日期', '收盘价', '涨跌幅', '超大单净流入-净占比', '大单净流入-净占比', '中单净流入-净占比', '小单净流入-净占比'
# ]]

# # for index,row in stock_fund_use.iterrows():
# # pprint(row)
# # break
# # stock_fund_use['pct'] = stock_fund_use['收盘价'] / stock_fund_use['收盘价'].shift(3) - 1
# # print(stock_fund_use[['日期','收盘价','涨跌幅','pct']])
# print(stock_fund_use)
