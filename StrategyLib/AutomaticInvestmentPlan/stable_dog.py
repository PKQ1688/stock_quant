"""
 Author       : adolf
 Date         : 2023-02-05 18:37:24
@LastEditors  : adolf
@LastEditTime : 2023-06-06 23:54:58
@FilePath     : /stock_quant/StrategyLib/AutomaticInvestmentPlan/stable_dog.py
"""

# "稳狗策略" 在股票下跌后进行买入，股票上涨后进行卖出
from dataclasses import asdict, dataclass

import baostock as bs
import pandas as pd

# import pandas_ta as ta
from finta import TA


@dataclass
class Account:
    date: str = ""
    buy_index: int = 0
    buy_date: str = ""
    assert_num: float = 0
    account: float = 0
    put: float = 0
    put_in: float = 0
    rate: float = 0


def get_AI_plan_result(
    code="sh.600000",
    gap_days=3,
    first_buy_day="2019-01-05",
    want_rate=1.1,
    if_intelli=True,
    threshold=500000,
):
    try:
        data = pd.read_csv(f"Data/RealData/Baostock/day/{code}.csv")
    except Exception as e:
        print(e)
        bs.login()
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount",
            start_date=first_buy_day,
            end_date="2023-06-06",
            frequency="d",
            adjustflag="3",
        )
        # 打印结果集
        data_list = []
        while (rs.error_code == "0") & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        data = pd.DataFrame(data_list, columns=rs.fields)
        bs.logout()

    data = data.fillna("")
    # data = data[data["tradestatus"] == 1]
    data = data[["date", "code", "open", "high", "low", "close", "volume"]]

    macd_df = TA.MACD(data)
    data["MACD"], data["SIGNAL"] = [macd_df["MACD"], macd_df["SIGNAL"]]
    data["HISTOGRAM"] = data["MACD"] - data["SIGNAL"]

    data = pd.concat([data, macd_df])
    data = data[data["date"] >= first_buy_day]
    # print(data)
    data.reset_index(inplace=True, drop=True)
    # first_buy_day=data.loc[0,"date"]
    my_account = Account()
    rate_list = []
    for index, row in data.iterrows():
        times = 1
        my_account.put = 0
        buy_flag = True
        if if_intelli:
            # if row.HISTOGRAM > 0 or (index >2 and  data.loc[index-1].HISTOGRAM >0 and data.loc[index-2].HISTOGRAM >0 ):
            if index != 0 and (row.HISTOGRAM > 0 and row.close > row.open):
                print(row.date + "macd 红柱,或今日上涨不投")
                buy_flag = False
            if my_account.put_in != 0:
                if my_account.rate > want_rate * 0.95:
                    print(
                        f"{row.date} + 目前收益率已到达高水位线{want_rate * 0.95}，不再买入"
                    )
                    buy_flag = False
                if my_account.rate < 0.9:
                    times = min(int(my_account.put_in / 1000 / 6), 5)
                if my_account.rate < 0.8:
                    times = min(int(my_account.put_in / 1000 / 3), 10)
                if my_account.rate < 0.7:
                    times = min(int(my_account.put_in / 1000 / 2), 20)
        if my_account.put_in > threshold:
            print(f"{row.date} + 目前投入已达到{threshold}，需要卖出一半股票以降低仓位")
            buy_flag = False
            sell_amount = my_account.put_in / 2
            my_account.put = -sell_amount
            my_account.put_in -= sell_amount
            my_account.assert_num = my_account.assert_num - sell_amount / row.close

        if index == 0 or (index - my_account.buy_index >= gap_days and buy_flag):
            print("index:%s" % index)
            money = 1000 * times
            my_account.buy_index = index
            my_account.buy_date = row.date
            my_account.assert_num += money / row.close
            my_account.put_in += money
            my_account.put = money

        my_account.date = row.date
        my_account.account = row.close * my_account.assert_num
        if my_account.put_in != 0:
            my_account.rate = my_account.account / my_account.put_in
            rate_list.append(asdict(my_account).copy())
        if my_account.rate > want_rate:
            print("my_account.rate ", my_account.rate)
            break

    # print(my_account)
    # print(rate_list)
    rate_df = pd.DataFrame(rate_list)
    # print(rate_df)
    data = data[data["date"] <= my_account.date]
    return rate_df, data


code = "sz.002044"
gap_days = 1
first_buy_day = "2021-02-22"
want_rate = 1.1

res, stock = get_AI_plan_result(
    code=code,
    gap_days=int(gap_days),
    first_buy_day=first_buy_day,
    want_rate=float(want_rate),
    threshold=500000,
)

print(res)
