"""
Description: 
Author: adolf
Date: 2022-08-29 22:22:52
LastEditTime: 2022-08-29 22:22:52
LastEditors: adolf
"""
import dask
import dask.dataframe as dd

from MachineLearning.data_process.base_data import get_handle_data

# def dask_one_data_process(data_path):
#     data = dd.read_csv(data_path)
#     # data = data.drop(columns=["code", "pct"])
#     data = data[["open", "high", "low", "close", "volume", "turn", "pctChg"]]
#     print(data.tail())
#     # data.to_csv(data_path, index=False)


# dask_one_data_process("Data/RealData/hfq/000001.csv")

import time

start_time = time.time()
res_df = get_handle_data("000001.csv")

print("use time: {}".format(time.time() - start_time))
print(res_df.tail())

# with pathos.multiprocessing.ProcessingPool(8) as p:
#     result = list(
#         tqdm(
#             p.imap(self.cal_one_data, self.all_data_list),
#             total=len(self.all_data_list),
#             desc="运行全体数据",
#         )
#     )
