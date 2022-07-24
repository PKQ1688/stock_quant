<!--
 * @Description: 
 * @Author: adolf
 * @Date: 2022-01-04 20:52:13
 * @LastEditTime: 2022-07-24 13:58:29
 * @LastEditors: adolf
-->
# stock_quant
用于股票量化策略的测试

## 零、TODO LIST
- [ ] 支持概念板块的历史数据获取
- [ ] 完善缠论对股票的分析

## 一、项目的基础设定
### 1.1 用于控制台使用代理
```
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
```

### 1.2 设置python运行路径
```
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### 1.3 设置python不生成pyc(__pycache__)
```
export PYTHONDONTWRITEBYTECODE=1
```

## 二、获取需要使用到的基本数据
### 2.1 获取基础股票数据
&nbsp; 从东方财富官网获取个股的历史数据，包含前复权，后复权，未复权。
```
ptyhon GetBaseData/get_dc_data.py
```
### 2.2 获取基础的个股资金流量数据
&nbsp; 从东方财富官网获取不同股票的近100日的超大、大、中、小单数据变化。
```
python GetBaseData/get_cash_flow_data.py
```
### 2.3 获取不同板块的历史数据
&nbsp; 从东方财富官网获取板块的历史数据。
目前仅支持行业板块，暂不支持概念板块的数据
```
python GetBaseData/get_board_data.py
```

## 如果要使用前端展示缠论结果
```
streamlit run StrategyLib/ChanStrategy/automatic_drawing.py
```
