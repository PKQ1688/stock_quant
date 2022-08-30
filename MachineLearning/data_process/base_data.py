"""
Description: 
Author: adolf
Date: 2022-08-21 15:26:58
LastEditTime: 2022-08-21 15:27:02
LastEditors: adolf
"""
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
import ray

# pd.set_option('display.max_columns', None)


def init_dict():
    new_data_dict = {}

    new_data_dict["code"] = []
    for i in range(60):
        new_data_dict["open_{}".format(i)] = []
        new_data_dict["high_{}".format(i)] = []
        new_data_dict["low_{}".format(i)] = []
        new_data_dict["close_{}".format(i)] = []
        new_data_dict["volume_{}".format(i)] = []
        new_data_dict["turn_{}".format(i)] = []
    new_data_dict["pct"] = []
    return new_data_dict


@ray.remote
def get_handle_data(data_name):
    try:
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
            tmp_data = data_t[index - 60 : index]

            tmp_data[["open"]].apply(
                lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            ).copy()
            tmp_data[["high"]].apply(
                lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            ).copy()
            tmp_data[["low"]].apply(
                lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            ).copy()
            tmp_data[["close"]].apply(
                lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            ).copy()
            tmp_data[["volume"]].apply(
                lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            ).copy()
            tmp_data[["turn"]].apply(lambda x: x / 100).copy()

            # print(tmp_data)
            # exit()

            open_list = tmp_data.open.values.tolist()
            close_list = tmp_data.close.values.tolist()
            high_list = tmp_data.high.values.tolist()
            low_list = tmp_data.low.values.tolist()
            volume_list = tmp_data.volume.values.tolist()
            turn_list = tmp_data.turn.values.tolist()

            new_data_dict["code"].append(row.code)

            for i in range(60):
                new_data_dict.get("open_{}".format(i)).append(open_list[i])
                new_data_dict.get("high_{}".format(i)).append(high_list[i])
                new_data_dict.get("low_{}".format(i)).append(low_list[i])
                new_data_dict.get("close_{}".format(i)).append(close_list[i])
                new_data_dict.get("volume_{}".format(i)).append(volume_list[i])
                new_data_dict.get("turn_{}".format(i)).append(turn_list[i])

            new_data_dict["pct"].append(data_t.loc[index + 1, "pctChg"])
            # break

        # pd.set_option("display.max_columns", None)
        res_data = pd.DataFrame(new_data_dict)
        # print(res_data)
        res_data.to_csv(f"Data/HandleData/hfq_stock/handle_{data_name}", index=False)
        return res_data
    except:
        print(data_name)
        return None


# get_handle_data("000001.csv")

if __name__ == "__main__":
    import os

    ray.init()

    # for data_name in os.listdir("Data/RealData/hfq"):
    #     print(data_name)
    #     get_handle_data.remote(data_name)
    #     break

    futures = [get_handle_data.remote(code) for code in os.listdir("Data/RealData/hfq")]

    def to_iterator(obj_ids):
        while obj_ids:
            done, obj_ids = ray.wait(obj_ids)
            yield ray.get(done[0])

    for x in tqdm(to_iterator(futures), total=len(os.listdir("Data/RealData/hfq"))):
        pass
