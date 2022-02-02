# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/2 14:50
# @Author  : Adolf
# @File    : basic_tools.py
# @Function:
from StrategyLib.ChanStrategy.basic_structure import RawBar, NewBar, FX
from StrategyLib.ChanStrategy.basic_enum import Direction, Mark


def remove_include(k1: NewBar, k2: NewBar, k3: RawBar):
    """去除包含关系：输入三根k线，其中k1和k2为没有包含关系的K线，k3为原始K线"""
    if k1.high < k2.high:
        direction = Direction.Up
    elif k1.high > k2.high:
        direction = Direction.Down
    else:
        k4 = NewBar(symbol=k3.symbol, id=k3.id, freq=k3.freq, dt=k3.dt, open=k3.open,
                    close=k3.close, high=k3.high, low=k3.low, vol=k3.vol, elements=[k3])
        return False, k4

    # 判断 k2 和 k3 之间是否存在包含关系，有则处理
    if (k2.high <= k3.high and k2.low >= k3.low) or (k2.high >= k3.high and k2.low <= k3.low):
        if direction == Direction.Up:
            high = max(k2.high, k3.high)
            low = max(k2.low, k3.low)
            dt = k2.dt if k2.high > k3.high else k3.dt
        elif direction == Direction.Down:
            high = min(k2.high, k3.high)
            low = min(k2.low, k3.low)
            dt = k2.dt if k2.low < k3.low else k3.dt
        else:
            raise ValueError

        # 成交量相加的逻辑不是缠论本身的逻辑
        vol = k2.vol + k3.vol

        # 因为缠论只考虑最高和最低,所以这里的开盘和收盘价逻辑属于自由发挥
        # 这里的逻辑是去除引线，但保持k线颜色不变
        if k3.open > k3.close:
            _open = high
            _close = low
        else:
            _open = low
            _close = high

        # 这里可能合并的k线过多，先取后100根k线作为参考标准
        # elements = [x for x in k2.elements[-100:] if x.dt != k3.dt] + [k3]
        elements = [x for x in k2.elements if x.dt != k3.dt] + [k3]

        k4 = NewBar(symbol=k3.symbol, id=k2.id, freq=k2.freq, dt=dt, open=_open,
                    close=_close, high=high, low=low, vol=vol, elements=elements)

        return True, k4
    else:
        k4 = NewBar(symbol=k3.symbol, id=k3.id, freq=k3.freq, dt=k3.dt, open=k3.open,
                    close=k3.close, high=k3.high, low=k3.low, vol=k3.vol, elements=[k3])
        return False, k4


def check_fx(k1: NewBar, k2: NewBar, k3: NewBar):
    """查找分型"""
    fx = None
    if k1.high < k2.high > k3.high and k1.low < k2.low > k3.low:
        power = "强" if k3.low < k1.low else "弱"
        fx = FX(symbol=k2.symbol, dt=k2.dt, mark=Mark.G, high=k2.high, low=min(k1.low, k3.low),
                fx=k2.high, elements=[k1, k2, k3], power=power)

    if k1.low > k2.low < k3.low and k1.high > k2.high < k3.high:
        power = "强" if k3.high > k1.high else "弱"
        fx = FX(symbol=k2.symbol, dt=k2.dt, mark=Mark.D, low=k2.low, high=max(k1.high, k3.high),
                fx=k2.low, elements=[k1, k2, k3], power=power)

    return fx


