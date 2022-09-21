"""
Description: 
Author: adolf
Date: 2022-08-29 22:22:52
LastEditTime: 2022-08-29 22:22:52
LastEditors: adolf
"""
import time

# import dask
# import dask.dataframe as dd

from MachineLearning.data_process.base_data import get_handle_data

# def dask_one_data_process(data_path):
#     data = dd.read_csv(data_path)
#     # data = data.drop(columns=["code", "pct"])
#     data = data[["open", "high", "low", "close", "volume", "turn", "pctChg"]]
#     print(data.tail())
#     # data.to_csv(data_path, index=False)


# dask_one_data_process("Data/RealData/hfq/000001.csv")


# start_time = time.time()
# res_df = get_handle_data("000001.csv")

# print("use time: {}".format(time.time() - start_time))
# print(res_df.tail())

if __name__ == "__main__":
    import os
    import pathos
    from tqdm.auto import tqdm

    start_time = time.time()

    all_data_list = os.listdir("Data/RealData/hfq")
    with pathos.multiprocessing.ProcessingPool(8) as p:
        result = list(
            tqdm(
                p.imap(get_handle_data, all_data_list),
                total=len(all_data_list),
                desc="使用python进程池对数据进行预处理",
            )
        )
    
    print("use time: {}".format(time.time() - start_time))
