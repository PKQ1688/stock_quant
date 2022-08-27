"""
Description: 
Author: adolf
Date: 2022-08-25 00:10:23
LastEditTime: 2022-08-25 22:28:07
LastEditors: adolf
"""
from random import shuffle
import numpy as np
import dask.dataframe as dd
import lightgbm as lgb

import pickle

from pathlib import Path
from sklearn.model_selection import train_test_split
from dask_ml.model_selection import train_test_split as dask_train_test_split
from sklearn.metrics import accuracy_score

filename = Path("Data/HandleData/hfq_stock", "handle_00000*.csv")
# print(filename)

df = dd.read_csv(filename)
# print(df.head())
# print(len(df))

x = df.drop(columns=["label"])
y = df["label"]
# train,test = train_test_split(df,test_size=0.2)
x_train, x_test, y_train, y_test = dask_train_test_split(
    x, y, test_size=0.2, shuffle=True
)

# print(x_train.head())
# print(x_test.head())

# print(len(x_train))
# print(len(x_test))
# exit()
# msk = np.random.rand(len(df)) < 0.8
# train = df[msk]
# test = df[~msk]

# x_train = train.drop(columns=["label"])
# y_train = train["label"]


model = lgb.LGBMClassifier()
model.fit(x_train, y_train)

# x_test = test.drop(columns=["label"])
# y_test = test["label"]

# print(model.predict(x))
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("accuarcy: %.2f%%" % (accuracy * 100.0))

with open('MachineLearning/lgb_model.pkl', 'rb') as fout:
    pickle.dump(model, fout)