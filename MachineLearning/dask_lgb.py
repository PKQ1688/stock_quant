"""
Description: 
Author: adolf
Date: 2022-08-25 00:10:23
LastEditTime: 2022-08-25 22:28:07
LastEditors: adolf
"""
import dask.array as da
from distributed import Client, LocalCluster
from sklearn.datasets import make_blobs

import lightgbm as lgb

print("loading data...")

X, y = make_blobs(n_samples=10000, n_features=10, centers=3)

print("initializing dask cluster...")

cluster = LocalCluster(n_workers=2)
client = Client(cluster)

dX = da.from_array(X, chunks=(100, 50))
dy = da.from_array(y, chunks=(100,))

print("beginning training")

dask_model = lgb.DaskLGBMClassifier(n_estimators=10)
dask_model.fit(dX, dy)
assert dask_model.fitted_

print("done training")