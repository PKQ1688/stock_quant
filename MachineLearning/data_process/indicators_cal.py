"""
Author       : adolf
Date         : 2023-01-09 22:34:00
LastEditors  : adolf adolf1321794021@gmail.com
LastEditTime : 2023-01-14 19:32:41
FilePath     : /stock_quant/MachineLearning/data_process/indicators_cal.py
"""

import warnings

import pandas as pd
import pandas_ta as ta

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def cal_indicators(filename):
    # print(filename.name)
    try:
        data = pd.read_csv(filename)
        # data["pct"] = data.close.pct_change()

        # 计算5日均线和10日均线
        data["sma5"] = ta.sma(data.close, length=5)
        data["sma10"] = ta.sma(data.close, length=10)

        # 计算5日均线和10日均线的交叉
        # data["ma_long"] = ta.cross(data.sma5, data.sma10)
        # data["ma_short"] = ta.cross(data.sma10, data.sma5)

        # 计算macd的值
        data[["macd", "histogram", "signal"]] = ta.macd(
            data.close, fast=12, slow=26, signal=9
        )

        # # 计算bolinger band的值
        # data[["lower", "mid", "upper", "width", "percent"]] = ta.bbands(
        #     data.close, length=20, std=2
        # )

        # 计算atr的值
        data["atr"] = ta.atr(data.high, data.low, data.close, length=14)

        data["pct"] = data.pctChg.shift(-1)
        print(data.tail(30))
        exit()

        data.drop(
            ["date", "amount", "amplitude", "priceChg", "code", "name"],
            axis=1,
            inplace=True,
        )

        # print(data.tail(30))
        data.dropna(inplace=True)
        data.to_csv(f"Data/HandleData/indicator_data/{filename.name}", index=False)
        return data
    except Exception as e:
        print(e)
        print(filename.name)
        return None


if __name__ == "__main__":
    # import dask
    import pathlib

    from dask.distributed import Client, LocalCluster, progress

    client = Client(LocalCluster(n_workers=4, threads_per_worker=1, memory_limit="2GB"))

    futures = []

    file_path = pathlib.Path("Data/RealData/hfq/")
    for filename in file_path.glob("*.csv"):
        # print(filename)
        future = client.submit(cal_indicators, filename)
        # break
        futures.append(future)
        # if len(futures) > 10:
        # break

    progress(futures)
    # print(futures[0].result())
