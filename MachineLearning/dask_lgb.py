"""
 Author       : adolf
 Date         : 2022-11-19 21:05:12
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-23 20:09:54
 FilePath     : /stock_quant/MachineLearning/dask_lgb.py
"""
import dask.array as da
import lightgbm as lgb
from distributed import Client, LocalCluster
import pickle
# from sklearn.datasets import make_regression
# from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_blobs


# from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
    pass

    # cluster = LocalCluster(n_workers=2)
    # client = Client()
    # # client = Client("tcp://127.0.0.1:8786")

    # X, y = make_regression(n_samples=1000, n_features=50)
    # dX = da.from_array(X, chunks=(100, 50))
    # dy = da.from_array(y, chunks=(100,))

    # dask_model = lgb.DaskLGBMRegressor(n_estimators=10)
    # dask_model.fit(dX, dy)

    # with open("model/dask-model.pkl", "wb") as f:
    #     pickle.dump(dask_model, f)

    # with open("model/dask-model.pkl", "rb") as f:
    #     dask_model = pickle.load(f)

    # preds = dask_model.predict(dX)

    # print("computing MSE")

    # preds_local = preds.compute()
    # actuals_local = dy.compute()
    # mse = mean_squared_error(actuals_local, preds_local)

    # print(f"MSE: {mse}")

    #########################################################################################

    # # 准备数据

    # X, y = make_blobs(n_samples=1000, n_features=50, centers=3)

    # dX = da.from_array(X, chunks=(100, 50))
    # dy = da.from_array(y, chunks=(100,))

    # # 训练
    # params={
    #     'learning_rate':0.1,
    #     'lambda_l1':0.1,
    #     'lambda_l2':0.2,
    #     'max_depth':6,
    #     'objective':'multiclass',
    #     'num_class':4,  
    # }
    # dask_model = lgb.DaskLGBMClassifier(n_estimators=10)
    # dask_model.fit(dX, dy,params=params)

    # # 1、AUC
    # y_pred_pa = clf.predict(X_test)  # !!!注意lgm预测的是分数，类似 sklearn的predict_proba
    # y_test_oh = label_binarize(y_test, classes= [0,1,2,3])
    # print '调用函数auc：', roc_auc_score(y_test_oh, y_pred_pa, average='micro')

    # #  2、混淆矩阵
    # y_pred = y_pred_pa .argmax(axis=1)
    # confusion_matrix(y_test, y_pred )

    # #  3、经典-精确率、召回率、F1分数
    # precision_score(y_test, y_pred,average='micro')
    # recall_score(y_test, y_pred,average='micro')
    # f1_score(y_test, y_pred,average='micro')

    # # 4、模型报告
    # print(classification_report(y_test, y_pred))

    # # 保存模型
    # joblib.dump(clf, './model/lgb.pkl')