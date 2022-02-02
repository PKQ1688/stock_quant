# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/2 14:50
# @Author  : Adolf
# @File    : basic_tools.py
# @Function:

from StrategyLib.ChanStrategy.BasicChan.basic_structure import RawBar, NewBar, FX, BI
from StrategyLib.ChanStrategy.BasicChan.basic_enum import Direction, Mark
from Utils.ShowKline.chan_plot import kline_pro
from typing import List


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


def check_fxs(bars: List[NewBar]) -> List[FX]:
    """输入一串无包含关系K线，查找其中所有分型"""
    fxs = []
    for i in range(1, len(bars) - 1):
        fx: FX = check_fx(bars[i - 1], bars[i], bars[i + 1])
        if isinstance(fx, FX):
            # TODO 按照缠论定义重新编写顶底分型的代码
            # 按照缠论本身定义如果出现新的顶底需要和原来的顶底进行比较
            # if len(fxs) >= 2 and fx.mark == fxs[-1].mark:
            #     if fx.mark == "顶分型" and fx.high > fxs[-1].high:
            #         fxs.pop()
            #         fxs.append(fx)
            #
            # fxs.append(fx)
            # 这里可能隐含Bug，默认情况下，fxs本身是顶底交替的，但是对于一些特殊情况下不是这样，这是不对的。
            # 临时处理方案，强制要求fxs序列顶底交替,这会有问题
            if len(fxs) >= 2 and fx.mark == fxs[-1].mark:
                fxs.pop()
            fxs.append(fx)

    return fxs


def check_bi(bars: List[NewBar], bi_min_len: int = 7):
    """输入一串无包含关系K线，查找其中的一笔
    :param bars: 无包含关系K线列表
    :param bi_min_len: 一笔的最少无包含关系K线数量，7是老笔的要求,5是新笔的要求
    :return:
    """
    fxs = check_fxs(bars)
    if len(fxs) < 2:
        return None, bars

    fx_a = fxs[0]
    try:
        if fxs[0].mark == Mark.D:
            direction = Direction.Up
            fxs_b = [x for x in fxs if x.mark == Mark.G and x.dt > fx_a.dt and x.fx > fx_a.fx]
            if not fxs_b:
                return None, bars

            fx_b = fxs_b[0]
            for fx in fxs_b:
                if fx.high >= fx_b.high:
                    fx_b = fx

        elif fxs[0].mark == Mark.G:
            direction = Direction.Down
            fxs_b = [x for x in fxs if x.mark == Mark.D and x.dt > fx_a.dt and x.fx < fx_a.fx]
            if not fxs_b:
                return None, bars

            fx_b = fxs_b[0]
            for fx in fxs_b[1:]:
                if fx.low <= fx_b.low:
                    fx_b = fx

        else:
            raise ValueError

    except Exception as e:
        # traceback.print_exc()
        print(e)
        return None, bars

    # TODO 关于笔的逻辑部分存在问题
    bars_a = [x for x in bars if fx_a.elements[0].dt <= x.dt <= fx_b.elements[2].dt]
    bars_b = [x for x in bars if x.dt >= fx_b.elements[0].dt]

    # 判断fx_a和fx_b价格区间是否存在包含关系
    ab_include = (fx_a.high > fx_b.high and fx_a.low < fx_b.low) or (fx_a.high < fx_b.high and fx_a.low > fx_b.low)

    if len(bars_a) >= bi_min_len and not ab_include:
        fxs_ = [x for x in fxs if fx_a.elements[0].dt <= x.dt <= fx_b.elements[2].dt]
        bi = BI(symbol=fx_a.symbol, fx_a=fx_a, fx_b=fx_b, fxs=fxs_, direction=direction, bars=bars_a)
        return bi, bars_b
    else:
        return None, bars


class CZSC:
    def __init(self,
               bars: List[RawBar],
               # max_bi_count: int = 50,
               bi_min_len: int = 7,
               # get_signals: Callable = None,
               # signals_n: int = 0,
               verbose=False):
        """
        :param bars: K线数据
        # :param get_signals: 自定义的信号计算函数
        :param bi_min_len: 笔的最小长度，包括左右分型，默认值为 7，是缠论原文老笔定义的长度
        # :param signals_n: 缓存n个历史时刻的信号，0 表示不缓存；缓存的数据，主要用于计算信号连续次数
        # :param max_bi_count: 最大保存的笔数量
        #     默认值为 50，仅使用内置的信号和因子，不需要调整这个参数。
        #     如果进行新的信号计算需要用到更多的笔，可以适当调大这个参数。
        """
        self.verbose = verbose
        # self.max_bi_count = max_bi_count
        self.bi_min_len = bi_min_len
        # self.signals_n = signals_n
        self.bars_raw = []  # 原始K线序列
        self.bars_ubi = []  # 未完成笔的无包含K线序列
        self.bi_list: List[BI] = []
        self.symbol = bars[0].symbol
        self.freq = bars[0].freq
        # self.get_signals = get_signals
        # self.signals = None
        # self.signals_list = []

        for bar in bars:
            self.update(bar)

    def __repr__(self):
        return "<CZSC~{}~{}>".format(self.symbol, self.freq.value)

    def update(self, _bar: RawBar):
        """
        更新分析结果
        :param self:
        :param _bar: 单根K线对象
        :return:
        """
        # 如果是第一根K线或则最后一根k线
        if not self.bars_raw or _bar.dt != self.bars_raw[-1].dt:
            self.bars_raw.append(_bar)
            last_bars = [_bar]
        else:
            self.bars_raw[-1] = _bar
            last_bars = self.bars_ubi[-1].elements
            last_bars[-1] = _bar
            self.bars_ubi.pop(-1)

    def to_echarts(self, width: str = "1400px", height: str = '580px'):
        kline = [x.__dict__ for x in self.bars_raw]
        if len(self.bi_list) > 0:
            bi = [{'dt': x.fx_a.dt, "bi": x.fx_a.fx} for x in self.bi_list] + \
                 [{'dt': self.bi_list[-1].fx_b.dt, "bi": self.bi_list[-1].fx_b.fx}]
            fx = []
            for bi_ in self.bi_list:
                fx.extend([{'dt': x.dt, "fx": x.fx} for x in bi_.fxs[1:]])
        else:
            bi = None
            fx = None
        chart = kline_pro(kline, bi=bi, fx=fx, width=width, height=height,
                          title="{}-{}".format(self.symbol, self.freq.value))
        return chart
