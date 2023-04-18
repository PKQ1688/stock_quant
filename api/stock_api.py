import baostock as bs
from fastapi import FastAPI,Body,Response
import uvicorn


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
def push_records(records = Body(None) ):
    print(f"get records from browser:{records}")
    return "success"


@app.get('/index')
def func():
    with open('api/test.html', 'r', encoding='utf8') as file:
        content = file.read()
    # 4.返回响应数据
    return Response(content=content, media_type='text/html')



if __name__ == '__main__':

    uvicorn.run(app, host='172.22.67.15', port=9999)