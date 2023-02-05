"""
 Author       : adolf
 Date         : 2023-02-05 18:37:24
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-02-05 19:32:14
 FilePath     : /stock_quant/StrategyLib/AutomaticInvestmentPlan/stable_dog.py
"""

# "稳狗策略" 在股票下跌后进行买入，股票上涨后进行卖出
import pandas as pd
from dataclasses import dataclass
from typing import List

@dataclass
class RateReturn:
    date: str
    rate: float

@dataclass
class Account:
    buy_index: int = 0
    assert_num: float = 0
    account: float = 0
    put_in: float = 0
    rate_of_return: List(RateReturn)


data = pd.read_csv("Data/RealData/Baostock/day/sh.600000.csv")
data = data[data["tradestatus"] == 1]
data = data[["date","code","open","high","low","close","volume"]]
print(data)

first_buy_day = "2019-01-02"
data = data[data["date"] >= first_buy_day]
print(data)

my_account = Account()

for index,row in data.iterrows():
    print(row)
    if row.date == first_buy_day:
        # account = Account(buy_index=index,assert_num=1000/row.close,account=1000,put_in=1000)
        # print(account)
        my_account.buy_index = index
        my_account.assert_num = 1000/row.close
        my_account.put_in = 1000
        my_account.account = row.close*my_account.assert_num
    
    if index - my_account.buy_index == 3:
        my_account.buy_index = index
        my_account.assert_num += my_account.account/row.close
        my_account.put_in += 1000
        my_account.account = row.close*my_account.assert_num

    rate = my_account.account/my_account.put_in
    my_account.rate_of_return[row.date] = rate
    if rate > 1.1:
        break

print(my_account)