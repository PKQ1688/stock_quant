<!--
 * @Description: 
 * @Author: adolf
 * @Date: 2022-01-04 20:52:13
 * @LastEditTime: 2022-07-02 15:45:11
 * @LastEditors: adolf
-->
# stock_quant
用于股票量化策略的测试

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

## 如果要使用前端展示缠论结果
```
streamlit run StrategyLib/ChanStrategy/automatic_drawing.py
```
