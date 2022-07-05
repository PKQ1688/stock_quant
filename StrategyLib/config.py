'''
Description: 
Author: adolf
Date: 2022-07-05 19:44:36
LastEditTime: 2022-07-05 21:00:01
LastEditors: adolf
'''
ma5ma10_config = {
    "random_seed": 42,
    "log_level": "INFO",
    # "code_name": "600570",
    "code_name": "ALL_MARKET_100",
    # "code_name": ["600570", "002610", "300663"],
    # "start_stamp": "2020-01-01",
    # "end_stamp": "2020-12-31",
    # "show_data_path": "",
    # "strategy_params": {}
}

rumi_config = {
    "log_level": "INFO",
    # "code_name": "600570",
    "code_name": "ALL_MARKET_100",
    "start_stamp": "2005-01-01",
    "end_stamp": "2020-12-31",
    "strategy_params": {
        "sma_length": 10,
        "ema_length": 30,
        "aos_length": 60,
    }
}

rumi_params_config = {
    "log_level": "INFO",
    "code_name": "600570",
    "start_stamp": "2005-01-01",
    "end_stamp": "2020-12-31",
    "strategy_params": {
        "sma_length": [5, 10, 20, 30],
        "ema_length": [10, 20, 30, 60],
        "aos_length": [5, 10, 20, 30, 60],
    }
}

macd_deviate_config = {
    # "random_seed": 42,
    "log_level": "info",
    # "code_name": "600638",
    "code_name": "ALL_MARKET_100",
    # "code_name": ["600570", "002610", "300663","002612"],
    # "start_stamp": "2020-01-01",
    # "end_stamp": "2020-12-31",
    # "show_data_path": "",
    # "strategy_params": {}
}

macd_ma_config = {
    "log_level": "debug",
    "code_name": "000001",
    "take_profit": 0.02,
    "stop_loss": "",
}
