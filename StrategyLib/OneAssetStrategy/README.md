<!--
 * @Author       : adolf
 * @Date         : 2022-12-10 18:09:20
 * @LastEditors  : adolf adolf1321794021@gmail.com
 * @LastEditTime : 2022-12-10 20:24:18
 * @FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/README.md
-->
# 构建交易策略

### 1.Ma5Ma10
- 策略名称：双均线策略
- 策略逻辑：5日均线和10日均线策略,当5日均线上穿10日均线时买入,当5日均线下穿10日均线时卖出

### 2.EMA_Ma_Crossover
- 策略名称：均线动量策略
- 策略逻辑：使用EMA & MA Crossover 和 RSI 进行交易,具体策略如下:<br>
    1、MA > EMA;<br>
    2、close > open;<br>
    3、70 > RSI > 50;<br>
    4、close > Ma > Ema;<br>
    5、stop loss Ma;<br>
    6、profit-loss ratio 1:1.5

### 3.MACD_MA
- 策略名称：MACD结合均线策略
- 策略逻辑：<br>
    选股:1、60日线上 2、金叉 3、macd在0轴上方<br>
    买点：第一根绿线 <br>
    卖点:收益2个点则卖，最晚第三天卖


### 4.MacdDeviate
- 策略名称：MACD底背离策略
- 策略逻辑：使用MACD底背离策略，如果价格低点创下30日新低，并比上一个低点价格更低，但是对应的MACD值更高，则在其后的第一个MACD金叉买入，第一个MACD死叉卖出。
