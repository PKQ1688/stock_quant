"""
 Author       : adolf
 Date         : 2022-11-19 21:06:39
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-23 21:41:43
 FilePath     : /stock_quant/MachineLearning/data_process/dask_data.py
"""
import time

import dask

import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import traceback

# import dask.array as da
import pandas as pd

from dask.distributed import wait, progress
from dask.distributed import Client

import numpy as np

# from MachineLearning.data_process.base_data import get_handle_data


def init_dict():
    new_data_dict = {}

    # new_data_dict["code"] = []
    for i in range(60):
        new_data_dict["open_{}".format(i)] = []
        new_data_dict["high_{}".format(i)] = []
        new_data_dict["low_{}".format(i)] = []
        new_data_dict["close_{}".format(i)] = []
        new_data_dict["volume_{}".format(i)] = []
        new_data_dict["turn_{}".format(i)] = []
    new_data_dict["label"] = []
    return new_data_dict


def get_handle_data(data_name):
    try:
        # if True:
        data_t = pd.read_csv(f"Data/RealData/hfq/{data_name}", dtype={"code": str})
        data_t = data_t[
            ["date", "open", "high", "low", "close", "volume", "turn", "code", "pctChg"]
        ]

        new_data_dict = init_dict()

        for index, row in data_t.iterrows():
            if index < 60:
                continue
            # print(row)
            if index >= len(data_t) - 1:
                break
            tmp_data = data_t[index - 60 : index].copy()

            for feature in ["open", "high", "low", "close", "volume"]:
                tmp_data[feature] = tmp_data[[feature]].apply(
                    lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
                )

            # tmp_data["turn"] = tmp_data["turn"].apply(lambda x: x / 100)

            # print(tmp_data)
            # exit()

            open_list = tmp_data.open.values.tolist()
            close_list = tmp_data.close.values.tolist()
            high_list = tmp_data.high.values.tolist()
            low_list = tmp_data.low.values.tolist()
            volume_list = tmp_data.volume.values.tolist()
            turn_list = tmp_data.turn.values.tolist()

            # new_data_dict["code"].append(row.code)

            for i in range(60):
                new_data_dict.get("open_{}".format(i)).append(open_list[i])
                new_data_dict.get("high_{}".format(i)).append(high_list[i])
                new_data_dict.get("low_{}".format(i)).append(low_list[i])
                new_data_dict.get("close_{}".format(i)).append(close_list[i])
                new_data_dict.get("volume_{}".format(i)).append(volume_list[i])
                new_data_dict.get("turn_{}".format(i)).append(turn_list[i])

            # new_data_dict["pct"].append(data_t.loc[index + 1, "pctChg"])
            next_pct = data_t.loc[index + 1, "pctChg"]
            if next_pct > 7:
                # 超强                
                new_data_dict["label"].append(0)
            elif next_pct > 3:
                # 中强
                new_data_dict["label"].append(1)
            elif next_pct > 0:
                # 小强
                new_data_dict["label"].append(2)
            elif next_pct > -3:
                # 小弱
                new_data_dict["label"].append(3)
            elif next_pct > -7:
                # 中弱
                new_data_dict["label"].append(4)
            else:
                # 超弱
                new_data_dict["label"].append(5)

        res_data = pd.DataFrame(new_data_dict)
        # res_data = res_data.drop(columns=['code'])

        # print(res_data)
        if not os.path.exists(f"Data/HandleData/base_ohlcv_data"):
            os.mkdir(f"Data/HandleData/base_ohlcv_data")

        res_data.to_csv(f"Data/HandleData/base_ohlcv_data/{data_name}", index=False)
        return res_data
    except:
        # else:
        print(traceback.format_exc())
        print(data_name)
        res = {"errpr_message": traceback.format_exc(), "data_name": data_name}
        return os.getcwd()


# @dask.delayed
# def process_file(filename):
#     return get_handle_data(filename)


if __name__ == "__main__":
    import os

    start_time = time.time()

    all_data_list = os.listdir("Data/RealData/hfq")
    #     with pathos.multiprocessing.ProcessingPool(8) as p:
    #         result = list(
    #             tqdm(
    #                 p.imap(get_handle_data, all_data_list),
    #                 total=len(all_data_list),
    #                 desc="使用python进程池对数据进行预处理",
    #             )
    #         )

    # client = Client(n_workers=8, threads_per_worker=1, processes=True)
    client = Client("tcp://127.0.0.1:8786")

    ts = time.time()

    # contents = []
    # for filename in all_data_list:
    #     contents.append(process_file(filename))

    # print("submit use time: {}".format(time.time() - ts))

    # with ProgressBar():
    #     res = dask.compute(contents)[0]

    futures = []
    for filename in all_data_list:
        future = client.submit(get_handle_data, filename)
        futures.append(future)

    # total = client.map(reulst,futures)

    # progress(client.gather(futures))
    # results = [future.result() for future in futures]
    # with ProgressBar():
    # results = client.gather(futures)  # this can be faster
    # progress(client.gather(futures))
    # progress(results)
    progress(futures)
    print(futures[0].result())
    print("use time: {}".format(time.time() - start_time))
