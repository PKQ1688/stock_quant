# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/3 15:53
# @Author  : Adolf
# @File    : position_analysis.py
# @Function:
import pandas as pd

from Utils.base_utils import run_once


class BaseTransactionAnalysis:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def cal_max_down(df, pct_name="strategy_net", time_stamp="date"):
        res_df = df.copy()
        res_df['max2here'] = res_df[pct_name].expanding().max()
        res_df['dd2here'] = res_df[pct_name] / res_df['max2here'] - 1
        # 计算最大回撤，以及最大回撤结束时间
        end_date, max_draw_down = tuple(
            res_df.sort_values(by=['dd2here']).iloc[0][[time_stamp,
                                                        'dd2here']])
        # 计算最大回撤开始时间
        start_date = res_df[res_df[time_stamp] <= end_date].sort_values(
            by=pct_name, ascending=False).iloc[0][time_stamp]
        # 将无关的变量删除
        res_df.drop(['max2here', 'dd2here'], axis=1, inplace=True)
        return max_draw_down, start_date, end_date

    def cal_trader_analysis(self, data):
        # self.logger.debug(data)

        # 计算策略的收益率
        data['strategy_net'] = (1 + data['pct']).cumprod()
        data["pct_show"] = data["pct"].apply(lambda x: format(x, '.2%'))

        strategy_pct = data.tail(1)["strategy_net"].item()

        # 计算策略的成功率
        success_rate = len(data[data["pct"] > 0]) / len(data)

        # 计算策略的赔率
        odds = data["pct"].mean()

        # 计算盈亏比
        if len(data[data["pct"] > 0]) > 0:
            profit = data[data["pct"] > 0]["pct"].mean()
        else:
            profit = 0
        
        if len(data[data["pct"] < 0]) > 0:
            loss = data[data["pct"] < 0]["pct"].mean()
        else:
            loss = 0
    
        pl_ratio = profit * success_rate + loss * (1 - success_rate)

        # 计算策略的平均持股天数
        mean_holding_day = data["holding_time"].mean()

        # 计算总持有时间
        sum_holding_day = data["holding_time"].sum()

        # 统计策略的交易次数
        trade_nums = len(data)

        # strategy_annual_return = strategy_pct ** (250 / len(self.Data)) - 1

        # 统计策略的最大回撤
        strategy_max_draw_down, strategy_start_date, strategy_end_date = self.cal_max_down(
            df=data, pct_name="strategy_net", time_stamp="buy_date")

        result_dict = dict()
        result_dict["股票代码"]=data.loc[0,'pos_asset']
        result_dict["平均持有时间"] = mean_holding_day
        result_dict["交易次数"] = trade_nums
        result_dict["计算总持有时间"] = sum_holding_day

        result_dict["策略收益率"] = strategy_pct

        result_dict["策略成功率"] = success_rate
        result_dict["策略赔率"] = odds

        result_dict["策略最大回撤"] = strategy_max_draw_down

        result_dict["策略最大回撤开始时间"] = strategy_start_date
        result_dict["策略最大回撤结束时间"] = strategy_end_date

        result_dict["策略的盈亏比"] = pl_ratio
        # self.logger.info(result_dict)

        result_df = pd.DataFrame.from_dict(result_dict,
                                           orient='index',
                                           columns=["result"])
        self.logger.success(result_df)

        return result_df

    @run_once
    def cal_asset_analysis(self, data):
        # 计算标的收益率
        asset_pct = data.close[len(data) - 1] / data.close[0]

        # 计算标的年化
        asset_pct_annual_return = asset_pct**(250 / len(data)) - 1

        # 统计策略的最大回撤
        asset_max_draw_down, asset_start_date, asset_end_date = self.cal_max_down(
            df=data, pct_name="close", time_stamp="date")

        result_dict = dict()
        result_dict["标的收益率"] = asset_pct
        result_dict["标的年化"] = asset_pct_annual_return

        result_dict["标的最大回撤"] = asset_max_draw_down
        result_dict["标的最大回撤开始时间"] = asset_start_date
        result_dict["标的最大回撤结束时间"] = asset_end_date

        result_dict["标的交易时间"] = len(data)

        result_df = pd.DataFrame.from_dict(result_dict,
                                           orient='index',
                                           columns=["result"])
        # self.logger.debug(result_df)

        return result_df
    
    # TODO 展示股票交易结果买卖点
    def show_analysis_result(self):
        pass
