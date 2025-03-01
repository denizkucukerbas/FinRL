from finrl.train import train
from finrl.test import test
from finrl.config_tickers import DOW_30_TICKER
from finrl.config import INDICATORS
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from private import API_KEY, API_SECRET, API_BASE_URL

import numpy as np
import pandas as pd

ticker_list = DOW_30_TICKER
action_dim = len(ticker_list)
candle_time_interval = '5Min'  # '1Min'

env = StockTradingEnv

ERL_PARAMS = {"learning_rate": 3e-6,"batch_size": 2048, "gamma":  0.985,
        "seed":312,"net_dimension":512, "target_step":5000, "eval_gap":30,
        "eval_times":1} 
#if you want to use larger datasets (change to longer period), and it raises error, 
#please try to increase "target_step". It should be larger than the episode steps. 

start_date = '2022-6-11'
end_date = '2022-9-1'
model_name='ppo'
MODEL_IDX = f'{model_name}_{start_date}_{end_date}'

if __name__ == "__main__":
        train(start_date = start_date, 
        end_date = end_date,
        ticker_list = ticker_list, 
        data_source = 'alpaca',
        time_interval= candle_time_interval, 
        technical_indicator_list= INDICATORS,
        drl_lib='elegantrl',
        #       drl_lib='rllib', 
        #       drl_lib='stable_baselines3', 
        env=env,
        model_name=model_name, 
        API_KEY = API_KEY, 
        API_SECRET = API_SECRET, 
        API_BASE_URL = API_BASE_URL,
        erl_params=ERL_PARAMS,
        cwd=f'./papertrading_erl/{MODEL_IDX}', #current_working_dir
        wandb=False,
        break_step=1e7)

