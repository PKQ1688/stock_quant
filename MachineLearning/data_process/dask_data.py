'''
Description: 
Author: adolf
Date: 2022-08-29 22:46:23
LastEditTime: 2022-08-29 22:47:26
LastEditors: adolf
'''
"""
Description: 
Author: adolf
Date: 2022-08-29 22:22:52
LastEditTime: 2022-08-29 22:22:52
LastEditors: adolf
"""
import dask
import dask.dataframe as dd


def dask_one_data_process(data_path):
    data = dd.read_csv(data_path)
    # data = data.drop(columns=["code", "pct"])
    data = data[["open", "high", "low", "close", "volume", "turn", "pctChg"]]
    print(data.head())
    # data.to_csv(data_path, index=False)

dask_one_data_process("Data/RealData/hfq/000001.csv")