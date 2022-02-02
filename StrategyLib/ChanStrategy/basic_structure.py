# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/2/2 14:56
# @Author  : Adolf
# @File    : basic_structure.py
# @Function:
from dataclasses import dataclass
from datetime import datetime
from StrategyLib.ChanStrategy.basic_enum import Freq, Mark

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
