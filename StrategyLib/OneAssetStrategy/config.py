"""
 Author       : adolf
 Date         : 2022-11-15 22:01:31
 LastEditors  : adolf adolf1321794021@gmail.com
 LastEditTime : 2022-11-15 22:01:32
 FilePath     : /stock_quant/StrategyLib/OneAssetStrategy/config.py
"""
"""
Description: 
Author: adolf
Date: 2022-07-05 19:44:36
LastEditTime: 2022-08-14 13:22:48
LastEditors: adolf
"""
ma5ma10_config = {
    "RANDOM_SEED": 42,
    "LOG_LEVEL": "INFO",
    "CODE_NAME": "600570",
    # "CODE_NAME": "ALL_MARKET_100",
    # "CODE_NAME": ["600570", "002610", "300663"],
    # "START_STAMP": "2020-01-01",
    # "END_STAMP": "2020-12-31",
    # "SHOW_DATA_PATH": "",
    # "STRATEGY_PARAMS": {}
}

rumi_config = {
    "LOG_LEVEL": "INFO",
    # "CODE_NAME": "600570",
    "CODE_NAME": "ALL_MARKET_100",
    "START_STAMP": "2005-01-01",
    "END_STAMP": "2020-12-31",
    "STRATEGY_PARAMS": {
        "sma_length": 10,
        "ema_length": 30,
        "aos_length": 60,
    },
}

rumi_params_config = {
    "LOG_LEVEL": "INFO",
    "CODE_NAME": "600570",
    "START_STAMP": "2005-01-01",
    "END_STAMP": "2020-12-31",
    "STRATEGY_PARAMS": {
        "sma_length": [5, 10, 20, 30],
        "ema_length": [10, 20, 30, 60],
        "aos_length": [5, 10, 20, 30, 60],
    },
}

macd_deviate_config = {
    # "RANDOM_SEED": 42,
    "LOG_LEVEL": "info",
    # "CODE_NAME": "600638",
    "CODE_NAME": "ALL_MARKET_100",
    # "CODE_NAME": ["600570", "002610", "300663","002612"],
    # "START_STAMP": "2020-01-01",
    # "END_STAMP": "2020-12-31",
    # "SHOW_DATA_PATH": "",
    # "STRATEGY_PARAMS": {}
}

macd_ma_config = {
    "LOG_LEVEL": "debug",
    "CODE_NAME": "000001",
    "take_profit": 0.02,
    "stop_loss": "",
}

ma_hl_config = {
    # "RANDOM_SEED": 42,
    "LOG_LEVEL": "DEBUG",
    "CODE_NAME": "600570",
    # "CODE_NAME": "ALL_MARKET_100",
    # "CODE_NAME": ["600570", "002610", "300663"],
    "START_STAMP": "2020-01-01",
    "END_STAMP": "2020-12-31",
    # "SHOW_DATA_PATH": "",
    "STRATEGY_PARAMS": {"sma_length": 20},
}
