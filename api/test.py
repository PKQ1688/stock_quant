

import requests

url = 'http://172.22.67.15:9999/stock_data'
json_param = {"code":"sh.600570","start_date":"2022-12-19","end_date":"2023-04-10","frequency":"d"}

response = requests.post(url, json=json_param)
print(response.text)