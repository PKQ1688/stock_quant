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
    print(data.head())
    # data = data.drop(columns=["code", "pct"])
    # data.to_csv(data_path, index=False)

dask_one_data_process("Data/HandleData/hfq_stock/handle_000001.csv")