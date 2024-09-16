"""
 Author       : adolf
 Date         : 2022-11-23 21:58:43
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-23 22:16:03
 FilePath     : /stock_quant/StrategyResearch/data_research/data_pipeline_dask.py
"""
import akshare as ak

from GetBaseData.ch_eng_mapping import ch_eng_mapping_dict


def get_original_data(code):
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq")
    stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)

    return stock_zh_a_hist_df[
        ["date", "open", "close", "high", "low", "volume", "turn", "pctChg"]
    ].iloc[::-1]


def base_data_pipeline(code):
    data = get_original_data(code)

    print(data)

    for index, row in data.iterrows():
        print(row)
        break


if __name__ == "__main__":

    base_data_pipeline("000001")
