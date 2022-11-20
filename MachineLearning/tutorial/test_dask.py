"""
 Author       : adolf
 Date         : 2022-11-18 00:16:44
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-20 22:23:19
 FilePath     : /stock_quant/MachineLearning/tutorial/test_dask.py
"""
import time
import dask
from dask.distributed import Client

from dask.diagnostics import ProgressBar

# from dask.distributed import progress


@dask.delayed
def process_file(x):
    time.sleep(1)
    return x * x


if __name__ == "__main__":

    ts = time.time()

    # 使用分布式进行计算
    client = Client("tcp://127.0.0.1:8786")

    # 使用本地进行计算
    # client = Client(n_workers=4)

    contents = []
    for index in range(20):
        # future = client.submit(process_file, index)
        contents.append(process_file(index))

    print("submit use time: {}".format(time.time() - ts))

    with ProgressBar():
        res = dask.compute(contents)[0]
        # res = contents.compute()
    print(type(res))
    print(res)

    print("all cost time :%s" % (time.time() - ts))
