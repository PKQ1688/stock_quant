"""
Description:
Author: adolf
Date: 2022-08-21 15:26:58
LastEditTime: 2022-08-21 15:27:02
LastEditors: adolf
"""

import os
import traceback

import numpy as np
import pandas as pd
import ray
from tqdm.auto import tqdm

# pd.set_option('display.max_columns', None)


def init_dict():
    new_data_dict = {}

    # new_data_dict["code"] = []
    for i in range(60):
        new_data_dict[f"open_{i}"] = []
        new_data_dict[f"high_{i}"] = []
        new_data_dict[f"low_{i}"] = []
        new_data_dict[f"close_{i}"] = []
        new_data_dict[f"volume_{i}"] = []
        new_data_dict[f"turn_{i}"] = []
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
                new_data_dict.get(f"open_{i}").append(open_list[i])
                new_data_dict.get(f"high_{i}").append(high_list[i])
                new_data_dict.get(f"low_{i}").append(low_list[i])
                new_data_dict.get(f"close_{i}").append(close_list[i])
                new_data_dict.get(f"volume_{i}").append(volume_list[i])
                new_data_dict.get(f"turn_{i}").append(turn_list[i])

            # new_data_dict["pct"].append(data_t.loc[index + 1, "pctChg"])
            next_pct = data_t.loc[index + 1, "pctChg"]
            if next_pct > 7:
                new_data_dict["label"].append("超强")
            elif next_pct > 3:
                new_data_dict["label"].append("中强")
            elif next_pct > 0:
                new_data_dict["label"].append("小强")
            elif next_pct > -3:
                new_data_dict["label"].append("小弱")
            elif next_pct > -7:
                new_data_dict["label"].append("中弱")
            else:
                new_data_dict["label"].append("超弱")

        res_data = pd.DataFrame(new_data_dict)
        # res_data = res_data.drop(columns=['code'])

        # print(res_data)
        if not os.path.exists("Data/HandleData/base_ohlcv_data"):
            os.mkdir("Data/HandleData/base_ohlcv_data")

        res_data.to_csv(f"Data/HandleData/base_ohlcv_data/{data_name}", index=False)
        return res_data
    except:
        # else:
        print(traceback.format_exc())
        print(data_name)
        return None


# get_handle_data("000001.csv")


@ray.remote
def ray_get_handle_data(data_name):
    return get_handle_data(data_name)


if __name__ == "__main__":
    import os
    import time

    ray.init()

    # for data_name in os.listdir("Data/RealData/hfq"):
    #     print(data_name)
    #     get_handle_data.remote(data_name)
    #     break

    start_time = time.time()

    futures = [
        ray_get_handle_data.remote(code) for code in os.listdir("Data/RealData/hfq")
    ]

    def to_iterator(obj_ids):
        while obj_ids:
            done, obj_ids = ray.wait(obj_ids)
            yield ray.get(done[0])

    for x in tqdm(to_iterator(futures), total=len(os.listdir("Data/RealData/hfq"))):
        pass

    print("use time: ", time.time() - start_time)
