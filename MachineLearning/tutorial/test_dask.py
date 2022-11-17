"""
 Author       : adolf
 Date         : 2022-11-18 00:16:44
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-18 00:18:54
 FilePath     : /stock_quant/MachineLearning/tutorial/test_dask.py
"""
import time
from dask.distributed import Client

def square(x):
    return x ** 2
def neg(x):
    return -x

# 使用分布式进行计算
# client = Client("192.168.1.15:8786", asynchronous=True)

# 使用本地进行计算
client = Client(asynchronous=True)

ts = time.time()
A = client.map(square, range(10000))
B = client.map(neg, A)
total = client.submit(sum, B)
print(total.result())
print("cost time :%s" % (time.time() - ts))
