# ！/usr/bin/env python
# @Project : stock_quant
# @Date    : 2022/2/2 14:56
# @Author  : Adolf
# @File    : basic_structure.py
# @Function:

from dataclasses import dataclass
from datetime import datetime

from StrategyLib.ChanStrategy.BasicChan.basic_enum import Direction, Freq, Mark
from Utils.TechnicalIndicators.basic_indicators import RSQ


@dataclass
class RawBar:
    """原始K线元素"""

    symbol: str
    id: int  # id 必须是升序
    dt: datetime
    freq: Freq
    open: float
    close: float
    high: float
    low: float
    vol: float
    amount: float = None


@dataclass
class NewBar:
    """去除包含关系后的K线元素"""

    symbol: str
    id: int  # id 必须是升序
    dt: datetime
    freq: Freq
    open: float
    close: float
    high: float
    low: float
    vol: float
    amount: float = None
    elements: list = None  # 存入具有包含关系的原始K线

    @property
    def raw_bars(self):
        return self.elements


@dataclass
class FX:
    symbol: str
    dt: datetime
    mark: Mark
    high: float
    low: float
    fx: float
    power: str = None
    elements: list = None

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
class FakeBI:
    """虚拟笔：主要为笔的内部分析提供便利"""

    symbol: str
    sdt: datetime
    edt: datetime
    direction: Direction
    high: float
    low: float
    power: float


def create_fake_bis(fxs: list[FX]) -> list[FakeBI]:
    """创建 fake_bis 列表
    :param fxs: 分型序列，必须顶底分型交替
    :return: fake_bis
    """
    if len(fxs) % 2 != 0:
        fxs = fxs[:-1]

    fake_bis = []
    for i in range(1, len(fxs)):
        fx1 = fxs[i - 1]
        fx2 = fxs[i]
        assert fx1.mark != fx2.mark
        if fx1.mark == Mark.D:
            fake_bi = FakeBI(
                symbol=fx1.symbol,
                sdt=fx1.dt,
                edt=fx2.dt,
                direction=Direction.Up,
                high=fx2.high,
                low=fx1.low,
                power=round(fx2.high - fx1.low, 2),
            )
        elif fx1.mark == Mark.G:
            fake_bi = FakeBI(
                symbol=fx1.symbol,
                sdt=fx1.dt,
                edt=fx2.dt,
                direction=Direction.Down,
                high=fx1.high,
                low=fx2.low,
                power=round(fx1.high - fx2.low, 2),
            )
        else:
            raise ValueError
        fake_bis.append(fake_bi)
    return fake_bis


@dataclass
class BI:
    symbol: str
    fx_a: FX = None  # 笔开始的分型
    fx_b: FX = None  # 笔开始的分型
    fxs: list = None  # 笔内部的分型列表
    direction: Direction = None
    bars: list[NewBar] = None

    def __post_init__(self):
        self.sdt = self.fx_a.dt
        self.edt = self.fx_b.dt

    def __repr__(self):
        return (
            f"BI(symbol={self.symbol}, sdt={self.sdt}, edt={self.edt},"
            f"direction={self.direction}, high={self.high}, low={self.low})"
        )

    # 定义一些附加属性，用的时候才会计算，提高效率
    # ======================================================================
    @property
    def fake_bis(self):
        return create_fake_bis(self.fxs)

    @property
    def high(self):
        return max(self.fx_a.high, self.fx_b.high)

    @property
    def low(self):
        return min(self.fx_a.low, self.fx_b.low)

    @property
    def power(self):
        return self.power_price

    @property
    def power_price(self):
        """价差力度"""
        return round(abs(self.fx_b.fx - self.fx_a.fx), 2)

    @property
    def power_volume(self):
        """成交量力度"""
        return sum([x.vol for x in self.bars[1:-1]])

    @property
    def change(self):
        """笔的涨跌幅"""
        c = round((self.fx_b.fx - self.fx_a.fx) / self.fx_a.fx, 4)
        return c

    @property
    def length(self):
        """笔的无包含关系K线数量"""
        return len(self.bars)

    @property
    def rsq(self):
        close = [x.close for x in self.raw_bars]
        return round(RSQ(close), 4)

    @property
    def raw_bars(self):
        """构成笔的原始K线序列"""
        x = []
        for bar in self.bars[1:-1]:
            x.extend(bar.raw_bars)
        return x


@dataclass
class ZS:
    symbol: str
    bis: list[BI]

    @property
    def sdt(self):
        """中枢开始时间"""
        return self.bis[0].sdt

    @property
    def edt(self):
        """中枢结束时间"""
        return self.bis[-1].edt

    @property
    def sdir(self):
        """中枢第一笔方向"""
        return self.bis[0].direction

    @property
    def edir(self):
        """中枢倒一笔方向"""
        return self.bis[-1].direction

    @property
    def zz(self):
        """中枢中轴"""
        return self.zd + (self.zg - self.zd) / 2

    @property
    def gg(self):
        """中枢最高点"""
        return max([x.high for x in self.bis])

    @property
    def zg(self):
        return min([x.high for x in self.bis[:3]])

    @property
    def dd(self):
        """中枢最低点"""
        return min([x.low for x in self.bis])

    @property
    def zd(self):
        return max([x.low for x in self.bis[:3]])

    def __repr__(self):
        return (
            f"ZS(sdt={self.sdt}, sdir={self.sdir}, edt={self.edt}, edir={self.edir}, "
            f"len_bis={len(self.bis)}, zg={self.zg}, zd={self.zd}, "
            f"gg={self.gg}, dd={self.dd}, zz={self.zz})"
        )
