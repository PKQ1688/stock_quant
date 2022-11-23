"""
 Author       : adolf
 Date         : 2022-11-21 22:03:29
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-21 22:11:59
 FilePath     : /stock_quant/MachineLearning/dask_sklearn.py
"""
from sklearn.ensemble import GradientBoostingClassifier
import sklearn.datasets
import dask_ml.datasets
from dask_ml.wrappers import ParallelPostFit

X, y = sklearn.datasets.make_classification(n_samples=1000,random_state=0)
clf = ParallelPostFit(estimator=GradientBoostingClassifier())
clf.fit(X, y)