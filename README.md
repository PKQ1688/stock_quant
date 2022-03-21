# stock_quant
用于股票量化策略的测试

# 用于控制台使用代理
export http_proxy="http://127.0.0.1:7890"

export https_proxy="http://127.0.0.1:7890"

# 设置python运行路径
export PYTHONPATH=$(pwd):$PYTHONPATH

# 如果要使用前端展示缠论结果
[//]: # (cd StrategyLib/ChanStrategy/)
streamlit run StrategyLib/ChanStrategy/automatic_drawing.py