"""
 Author       : adolf
 Date         : 2023-02-05 18:37:24
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-02-06 00:36:55
 FilePath     : /stock_quant/StrategyLib/AutomaticInvestmentPlan/stable_dog.py
"""

# "稳狗策略" 在股票下跌后进行买入，股票上涨后进行卖出
import pandas as pd
from dataclasses import dataclass, asdict


@dataclass
class Account:
    date: str = ""
    buy_index: int = 0
    buy_date: str = ""
    assert_num: float = 0
    account: float = 0
    put_in: float = 0
    rate: float = 0


data = pd.read_csv("Data/RealData/Baostock/day/sh.600000.csv")
data = data[data["tradestatus"] == 1]
data = data[["date", "code", "open", "high", "low", "close", "volume"]]

first_buy_day = "2019-01-02"
data = data[data["date"] >= first_buy_day]
# print(data)

my_account = Account()
rate_list = []

for index, row in data.iterrows():
    # import pdb
    # pdb.set_trace()
    # print(row)
    if row.date == first_buy_day:
        # account = Account(buy_index=index,assert_num=1000/row.close,account=1000,put_in=1000)
        # print(account)
        my_account.buy_index = index
        my_account.buy_date = row.date
        my_account.assert_num = 1000 / row.close
        my_account.put_in = 1000
    # my_account.account = row.close * my_account.assert_num

    if index - my_account.buy_index == 3:
        my_account.buy_index = index
        my_account.buy_date = row.date
        my_account.assert_num += 1000 / row.close
        my_account.put_in += 1000

    my_account.date = row.date
    my_account.account = row.close * my_account.assert_num
    my_account.rate = my_account.account / my_account.put_in
    rate_list.append(asdict(my_account).copy())
    if my_account.rate > 1.1:
        break
#
# print(my_account)
print(rate_list)
