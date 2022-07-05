'''
Description: 
Author: adolf
Date: 2022-07-03 17:29:10
LastEditTime: 2022-07-05 20:17:04
LastEditors: adolf
'''
from finta import TA
from BackTrader.base_back_trader import TradeStructure
from StrategyLib.config import macd_deviate_config

import numpy as np
from scipy.signal import argrelextrema


class MACDDeviate(TradeStructure):
    '''
    使用MACD底背离策略，如果价格低点创下30日新低，并比上一个低点价格更低，但是对应的MACD值更高，则在其后的第一个MACD金叉买入，第一个MACD死叉卖出。
    '''
    def __init__(self, config):
        super(MACDDeviate, self).__init__(config)

    def cal_technical_indicators(self, indicators_config):
        self.logger.debug('macd config:{}'.format(indicators_config))
        
        self.data["30_lowest"] = self.data.low.rolling(30).min()

        macd_df = TA.MACD(self.data)
        self.data["MACD"], self.data["SIGNAL"] = [macd_df["MACD"],macd_df["SIGNAL"]]
        self.data["HISTOGRAM"] = self.data['MACD'] - self.data['SIGNAL']

        # 获取到MACD金叉点和死叉点
        self.data.loc[(self.data['HISTOGRAM']>0)&(self.data['HISTOGRAM'].shift(1)<0),'trade'] = "LONG"
        self.data.loc[(self.data['HISTOGRAM']<0)&(self.data['HISTOGRAM'].shift(1)>0),'trade'] = "SHORT"

        self.data['price_state'] = 0
        # 寻找价格的极值点
        price_res = argrelextrema(self.data.low.values, np.less,order=1)[0].tolist()

        last_low_price = None
        last_macd = None
        for index in price_res:

            if last_low_price is not None and last_macd is not None:
                if self.data.loc[index,'low'] < last_low_price - 0.1 and \
                    self.data.loc[index,'MACD'] > last_macd  and \
                        self.data.loc[index,'low'] == self.data.loc[index,'30_lowest']:
                    self.data.loc[index,'price_state'] = 1
                    # self.logger.debug(self.data.loc[index,'date'])

            last_low_price = self.data.loc[index,'low']
            last_macd = self.data.loc[index,'MACD']    
        
        # self.logger.debug(self.data)

    def trading_algorithm(self):
        price_flag = 0
        for index,row in self.data.iterrows():
            if row['price_state'] == 1:
                price_flag = 1
    
            if row['trade'] == "LONG" and price_flag == 1:
                self.data.loc[index,'trade'] = "BUY"
                price_flag = 0
            elif row['trade'] == "SHORT":
                self.data.loc[index,'trade'] = "SELL"

if __name__ == '__main__':
    MACD_strategy = MACDDeviate(config=macd_deviate_config)
    MACD_strategy.run()