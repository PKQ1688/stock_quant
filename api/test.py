

import requests

url = 'http://172.22.67.15:9999/push_records'
json_param = [{"opt":"buy","date":"2021-09-09","price":1500},{"opt":"buy","date":"2021-09-09","price":3000}]
rec = {"user_id":"wxt","records":json_param}
response = requests.post(url, json=rec)
print(response.text)

