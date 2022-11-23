"""
 Author       : adolf
 Date         : 2022-11-22 23:18:30
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-23 21:52:01
 FilePath     : /stock_quant/MachineLearning/base_lgb.py
"""
#########################################################################################
# 模型 lightgbm
#########################################################################################
from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_squared_error

import lightgbm as lgb

print("Loading data...")
# load or create your dataset
regression_example_dir = Path("Data/HandleData/base_ohlcv_data")
df_train = pd.read_csv(
    str(regression_example_dir / "000001.csv"), sep=",", low_memory=False
)
df_test = pd.read_csv(
    str(regression_example_dir / "000002.csv"), sep=",", low_memory=False
)

maping_dict = {"超强": 0, "中强": 1, "小强": 2, "小弱": 3, "中弱": 4, "超弱": 5}

y_train = df_train["label"].map(maping_dict)
y_test = df_test["label"].map(maping_dict)
X_train = df_train.drop("label", axis=1)
X_test = df_test.drop("label", axis=1)

print(y_train)

# create dataset for lightgbm
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# specify your configurations as a dict
params = {
    "boosting_type": "gbdt",
    "objective": "multiclass",
    "metric": {"multi_logloss"},
    "num_leaves": 31,
    "learning_rate": 0.05,
    "num_class": 1,
}

print("Starting training...")
# train
gbm = lgb.train(
    params,
    lgb_train,
    num_boost_round=20,
    valid_sets=lgb_eval,
    callbacks=[lgb.early_stopping(stopping_rounds=5)],
)

print("Saving model...")
# save model to file
gbm.save_model("model.txt")

print("Starting predicting...")
# predict
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
# eval
rmse_test = mean_squared_error(y_test, y_pred) ** 0.5
print(f"The RMSE of prediction is: {rmse_test}")
