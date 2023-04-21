import os
import time
import socket

import pandas as pd
# from pyecharts.components import Table
from finta import TA
import baostock as bs
from fastapi import FastAPI, Body, Response
import uvicorn
from pymongo import MongoClient
from loguru import logger

app = FastAPI()
# mongo_config = {"host": "172.22.66.198", "port": 27017}
mongo_config = {"host": "localhost", "port": 27017}
db = MongoClient(mongo_config["host"], mongo_config["port"])["stock_db"]


@app.post("/stock_data")
def get_stock_data(
        code=Body("sh.600570"),
        start_date=Body("2022-12-19"),
        end_date=Body("2023-04-10"),
        frequency=Body("d")
):
    print(
        f"code:{code} start_date:{start_date} end_date:{end_date} frequency:{frequency}"
    )
    if os.path.exists("Data/Baostock/day/{}.csv".format(code)):
        data_df = pd.read_csv("Data/Baostock/day/{}.csv".format(code))

        data_df = data_df[data_df["date"] >= start_date]
        data_df = data_df[data_df["date"] <= end_date]

    else:
        bs.login()
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag="3",
        )
        # 打印结果集
        data_list = []
        while (rs.error_code == "0") & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        data_df = pd.DataFrame(data_list, columns=rs.fields)

        data_df["MA5"] = TA.SMA(data_df, period=5)
        data_df["MA10"] = TA.SMA(data_df, period=10)
        data_df["MA20"] = TA.SMA(data_df, period=20)
        data_df["MA30"] = TA.SMA(data_df, period=30)
        data_df["MA60"] = TA.SMA(data_df, period=60)

        macd_df = TA.MACD(data_df)
        macd_df["HISTOGRAM"] = macd_df["MACD"] - macd_df["SIGNAL"]
        data_df = pd.concat([data_df, macd_df], axis=1)

        bs.logout()

    base_data_list = [
        list(oclh) for oclh in zip(
            data_df["date"].tolist(),
            data_df["code"].tolist(),
            data_df["open"].tolist(),
            data_df["close"].tolist(),
            data_df["high"].tolist(),
            data_df["low"].tolist(),
            data_df["volume"].tolist(),
            data_df["amount"].tolist(),
        )
    ]
    macd_list = [
        list(macd) for macd in zip(
            data_df["MACD"].tolist(),
            data_df["SIGNAL"].tolist(),
            data_df["HISTOGRAM"].to_list(),
        )
    ]
    ma5_list = data_df["MA5"].tolist()
    ma10_list = data_df["MA10"].tolist()
    ma20_list = data_df["MA20"].tolist()
    ma30_list = data_df["MA30"].tolist()
    ma60_list = data_df["MA60"].tolist()

    logger.info("get data success!!!")
    return {
        "base_data": base_data_list,
        "macd": macd_list,
        "ma5": ma5_list,
        "ma10": ma10_list,
        "ma20": ma20_list,
        "ma30": ma30_list,
        "ma60": ma60_list
    }
    # return dict(
    #     base_data=base_data_list,
    #     macd=macd_list,
    #     ma5=ma5_list,
    #     ma10=ma10_list,
    #     ma20=ma20_list,
    #     ma30=ma30_list,
    #     ma60=ma60_list,
    # )


@app.post("/get_records")
def get_records(
        user_id=Body(None),
        start_date=Body(None),
        end_date=Body(None),
        stock_code=Body(None),
        count=Body(None),
):
    print("user_id:", user_id)
    filter = {}
    if user_id is not None and user_id != "":
        filter["user_id"] = user_id
    if start_date is not None and start_date != "":
        filter["date"] = {"$gte": start_date}
    if end_date is not None and end_date != "":
        if "date" in filter:
            filter["date"]["$lte"] = end_date
        else:
            filter["date"] = {"$lte": end_date}
    if stock_code is not None and stock_code != "":
        filter["stock_code"] = stock_code
    print(f"filter:{filter}")
    print(f"count:{count}")
    count = int(count)
    return_records = []
    profit_rate = 1
    stock_profit_rate = 1
    for history in db["play_records"].find(filter).limit(count):
        history.pop("_id")
        history.pop("records")
        profit_rate *= (1 + float(history["profit_rate"]))
        stock_profit_rate *= (1 + float(history["stock_profit_rate"]))
        print(f"profit_rate {profit_rate} stock_profit_rate {stock_profit_rate}")
        print("history: ", history)
        return_records.append(
            [history["user_id"], history["date"], history["stock_code"], float_to_pct(history["stock_profit_rate"]),
             float_to_pct(history["profit_rate"]), float_to_pct(history["over_profit"])])
    return {"records": return_records, "profit_rate": profit_rate - 1, "stock_profit_rate": stock_profit_rate - 1}


@app.post("/push_records")
def push_records(records=Body(None), user_id=Body(None), stock_code=Body(None), stock_profit_rate=Body(None)):
    print(f"get {user_id} records from browser:{records}")
    profit_rate = cal_profit_rate(records)
    today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    over_profit = float(profit_rate) - float(stock_profit_rate)
    db["play_records"].insert_one(
        {"user_id": user_id, "records": records, "profit_rate": profit_rate, "date": today, "stock_code": stock_code,
         "stock_profit_rate": stock_profit_rate, "over_profit": over_profit})
    return f"success,profit_rate is {float_to_pct(profit_rate)},over_profit is {float_to_pct(over_profit)}"


def float_to_pct(f):
    val = round(float(f) * 100, 2)
    return str(val) + "%"


def cal_profit_rate(records):
    profit_rate = 1
    assert len(records) % 2 == 0
    i = 0
    while i < len(records):
        profit_rate = records[i + 1]["price"] / records[i]["price"] * profit_rate
        i = i + 2
    return round((profit_rate - 1), 2)


@app.get("/index")
def func():
    with open("api/test.html", "r", encoding="utf8") as file:
        content = file.read()
    # 4.返回响应数据
    return Response(content=content, media_type="text/html")


@app.get("/hist")
def func():
    with open("api/hist.html", "r", encoding="utf8") as file:
        content = file.read()
    # 4.返回响应数据
    return Response(content=content, media_type="text/html")


if __name__ == '__main__':
    # 获取本机ip
    ip = socket.gethostbyname(socket.gethostname())
    print(f"ip : {ip}")
    uvicorn.run(app, host=ip, port=8501)
