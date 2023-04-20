import requests

def test_push_records():
    url = 'http://172.22.67.15:9999/push_records'
    json_param = [{"opt":"buy","date":"2021-09-09","price":1500},{"opt":"buy","date":"2021-09-09","price":3000}]
    rec = {"user_id":"wxt","records":json_param,"stock_code":"000111","stock_profit_rate":"10%","profit_rate":"100%"}
    response = requests.post(url, json=rec)
    print(f"response {response.text}")

def test_get_code_data():
    url = "http://172.22.67.15:9999/stock_data"
    rec = {
        "start_date": "2023-04-19",
        "end_date": "2023-04-19",
        "stock_code": "sz.002044",
    }
    response = requests.post(url, json=rec)
    print(len(response.json()))
    print(f"response {response.json()}")


def test_get_records():
    url = "http://172.22.67.15:9999/get_records"
    rec = {"user_id": "wxt", "start_date": "2023-04-19 14:15:10"}
    response = requests.post(url, json=rec)
    print(len(response.json()))
    print(f"response {response.json()}")
