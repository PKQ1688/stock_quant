<!--
 * @Description: 
 * @Author: adolf
 * @Date: 2022-01-04 20:52:13
 * @LastEditTime: 2022-07-02 16:58:19
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

### 1.3 设置python不生成pyc(__pycache__)
```
export PYTHONDONTWRITEBYTECODE=1
```

## 如果要使用前端展示缠论结果
```
streamlit run StrategyLib/ChanStrategy/automatic_drawing.py
```
