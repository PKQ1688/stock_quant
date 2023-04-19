import time

import baostock as bs
from fastapi import FastAPI,Body,Response
import uvicorn
from pymongo import MongoClient

app = FastAPI()
bs.login()

@app.post("/stock_data")
def get_stock_data(code = Body(None) , start_date= Body(None), end_date= Body(None),frequency= Body(None)):
    if start_date is None:
        start_date = "2022-12-19"
    if end_date is None:
        end_date = "2023-04-10"
    if frequency is None:
        frequency = "d"
    print(f"code:{code} start_date:{start_date} end_date:{end_date} frequency:{frequency}")
    rs = bs.query_history_k_data_plus(
        code,
        "date,open,close,high,low,volume,amount",
        start_date=start_date, end_date=end_date,
        frequency=frequency, adjustflag="1")
    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data = rs.get_row_data()
        for i in range(1,6):
            data[i] = round(float(data[i]), 3)
        data_list.append(data)
    # result = pd.DataFrame(data_list, columns=rs.fields)
    print(f"result:{data_list}")
    #将data_list的第1列的全部数据保留3位小数
    return data_list


@app.post("/push_records")
def push_records(records = Body(None),user_id = Body(None) ):
    print(f"request body : {Body}")
    print(f"get {user_id} records from browser:{records}")
    mongo_config = {"host": "172.22.66.198", "port": 27017}
    db = MongoClient(mongo_config["host"], mongo_config["port"])["stock_db"]
    profit_rate = cal_profit_rate(records)
    today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    db["play_records"].insert_one({"user_id":user_id,"records":records,"profit_rate":profit_rate,"date":today})
    return f"success,profit_rate is {profit_rate}"

def cal_profit_rate(records):
    profit_rate = 1
    assert len(records) % 2 == 0
    i = 0
    while i < len(records):
        profit_rate = records[i+1]["price"] / records[i]["price"] * profit_rate
        i = i + 2
    return str(round((profit_rate-1)*100,2)) +'%'

@app.get('/index')
def func():
    with open('api/test.html', 'r', encoding='utf8') as file:
        content = file.read()
    # 4.返回响应数据
    return Response(content=content, media_type='text/html')



if __name__ == '__main__':
    uvicorn.run(app, host='172.22.67.15', port=9999)
