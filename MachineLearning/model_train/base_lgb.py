"""
 Author       : adolf
 Date         : 2022-11-22 23:18:30
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2023-01-11 23:00:24
 FilePath     : /stock_quant/MachineLearning/model_train/base_lgb.py
"""
import json
import lightgbm as lgb
import pandas as pd
from sklearn.metrics import mean_squared_error

print("Load data...")
df_train = pd.read_csv("Data/HandleData/indicator_data/000001.csv")
df_test = pd.read_csv("Data/HandleData/indicator_data/000002.csv")

y_train = df_train["pctChg"].values
y_test = df_test["pctChg"].values

X_train = df_train.drop("pctChg", axis=1).values
X_test = df_test.drop("pctChg", axis=1).values

# print(X_train)

# create dataset for lightgbm
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# specify your configurations as a dict
params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'auc'},
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

print('Start training...')
# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

print('Save model...')
# save model to file
gbm.save_model('model.txt')

print('Start predicting...')
# predict
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
# eval
print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)