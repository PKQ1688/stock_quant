# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/2 14:56
# @Author  : Adolf
# @File    : basic_structure.py
# @Function:
from dataclasses import dataclass
from datetime import datetime
from StrategyLib.ChanStrategy.basic_enum import Freq, Mark, Direction

from typing import List


@dataclass
class RawBar:
    """原始K线元素"""
    symbol: str
    id: int  # id 必须是升序
    dt: datetime
    freq: Freq
    open: [float, int]
    close: [float, int]
    high: [float, int]
    low: [float, int]
    vol: [float, int]
    amount: [float, int] = None


@dataclass
class NewBar:
    """去除包含关系后的K线元素"""
    symbol: str
    id: int  # id 必须是升序
    dt: datetime
    freq: Freq
    open: [float, int]
    close: [float, int]
    high: [float, int]
    low: [float, int]
    vol: [float, int]
    amount: [float, int] = None
    elements: List = None  # 存入具有包含关系的原始K线

    @property
    def raw_bars(self):
        return self.elements


@dataclass
class FX:
    symbol: str
    dt: datetime
    mark: Mark
    high: [float, int]
    low: [float, int]
    fx: [float, int]
    power: str = None
    elements: List = None

    @property
    def new_bars(self):
        """构成分型的无包含关系K线"""
        return self.elements

    @property
    def raw_bars(self):
        """构成分型的原始K线"""
        res = []
        for e in self.elements:
            res.extend(e.raw_bars)
        return res


@dataclass
class BI:
    symbol: str
    fx_a: FX = None  # 笔开始的分型
    fx_b: FX = None  # 笔开始的分型
    fxs: List = None  # 笔内部的分型列表
    direction: Direction = None
    bars: List[NewBar] = None

    def __post_init__(self):
        self.sdt = self.fx_a.dt
        self.edt = self.fx_b.dt

    def __repr__(self):
        return f"BI(symbol={self.symbol}, sdt={self.sdt}, edt={self.edt}," \
               f"direction={self.direction}, high={self.high}, low={self.low})"

    # 定义一些附加属性，用的时候才会计算，提高效率
    # ======================================================================
    @property
    def high(self):
        return max(self.fx_a.high, self.fx_b.high)

    @property
    def low(self):
        return min(self.fx_a.low, self.fx_b.low)

