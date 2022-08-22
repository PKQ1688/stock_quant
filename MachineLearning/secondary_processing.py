"""
Description: 
Author: adolf
Date: 2022-08-21 22:40:28
LastEditTime: 2022-08-21 22:43:02
LastEditors: adolf
"""
import os
import pandas as pd
# import dask.dataframe as pd
from tqdm.auto import tqdm
import pathos


def secondary_processing_data(data_list=None):
    train_data_list = []
    if data_list is None:
        data_list = os.listdir("Data/HandleData/hfq_stock/")
    for data_name in tqdm(data_list):
        train_data = pd.read_csv(
            f"Data/HandleData/hfq_stock/{data_name}", dtype={"code": str}
        )
        # train_data['label'] =
        for index, row in train_data.iterrows():
            if row["pct"] > 7:
                train_data.loc[index, "label"] = "超强"
            elif row["pct"] > 3:
                train_data.loc[index, "label"] = "中强"
            elif row["pct"] > 0:
                train_data.loc[index, "label"] = "小强"
            elif row["pct"] > -3:
                train_data.loc[index, "label"] = "小弱"
            elif row["pct"] > -7:
                train_data.loc[index, "label"] = "中弱"
            else:
                train_data.loc[index, "label"] = "超弱"

        # train_data.to_csv(f"Data/HandleData/hfq_stock/{data_name}", index=False)
    
        train_data = train_data.drop(columns=['code','pct'])
        train_data.to_csv(f"Data/HandleData/hfq_stock/{data_name}",index=False)
        # train_data_list.append(train_data)
    
    # train_data_all = pd.concat(train_data_list, axis=0)
    # return train_data_all

secondary_processing_data()