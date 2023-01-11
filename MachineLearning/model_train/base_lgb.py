"""
 Author       : adolf
 Date         : 2022-11-22 23:18:30
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-01-10 23:51:05
 FilePath     : /stock_quant/MachineLearning/model_train/base_lgb.py
"""
from flaml.default import LGBMRegressor

estimator = LGBMRegressor()

estimator.fit(X_train, y_train)