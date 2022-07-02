'''
Description: 
Author: adolf
Date: 2022-07-02 14:18:51
LastEditTime: 2022-07-02 15:31:46
LastEditors: adolf
'''
import pandas as pd
from finta import TA
from tqdm.auto import tqdm

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Data/RealData/hfq/600570.csv")
print(df.head())