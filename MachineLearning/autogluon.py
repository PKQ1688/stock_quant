"""
Description: 
Author: adolf
Date: 2022-08-21 21:55:14
LastEditTime: 2022-08-21 22:22:12
LastEditors: adolf
"""
import os

# import pandas as pd
import dask.dataframe as dd
from autogluon.tabular import TabularPredictor
from tqdm.auto import tqdm

data_list = os.listdir("Data/HandleData/hfq_stock/")
# train_data = secondary_processing_data(data_list)
# train_data_list = []
# train_data_list = [
#     pd.read_csv(f"Data/HandleData/hfq_stock/{one}")
#     for one in tqdm(data_list, total=len(data_list))
# ]
# train_data = pd.concat(train_data_list, axis=0)
train_data = dd.read_csv(f"Data/HandleData/hfq_stock/handle_*.csv")
print(train_data.shape)
# print(train_data.shape)

label = "label"
model_path = "model/ohlcv60/"  # specifies folder to store trained models
predictor = TabularPredictor(label=label, path=model_path).fit(train_data)

# test_data = secondary_processing_data(data_list)

# y_test = test_data[label]  # values to predict
# test_data_nolab = test_data.drop(columns=[label])  # delete label column to prove we're not cheating

# predictor = TabularPredictor.load(model_path)
# y_pred = predictor.predict(test_data_nolab)
# print("Predictions:  \n", y_pred)
# perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred, auxiliary_metrics=True)
# print(perf)

# df = pd.concat([y_pred, y_test], axis=1)

# pd.set_option('display.max_rows', None)
# print(df)
