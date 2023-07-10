from finrl.train import train, load_df
from finrl.test import test
from finrl.config_tickers import *
from finrl.config import INDICATORS
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from finrl.plot import backtest_stats, backtest_plot, get_baseline, backtest_plot_v2, get_baseline_v2 # backtest_plot
from private import API_KEY, API_SECRET, API_BASE_URL

ticker_list = DOW_30_TICKER
# ticker_list = eval('DOW_30_TICKER')
# ticker_list = CHINESE_STOCK_TICKER[:30]

action_dim = len(ticker_list)
candle_time_interval = '1Min'  # '1Min'

env = StockTradingEnv

ERL_PARAMS = {"learning_rate": 3e-6, "batch_size": 2048, "gamma": 0.985,
              "seed": 312, "net_dimension": 512, "target_step": 5000, "eval_gap": 30,
              "eval_times": 1}
# train_start_date = '2019-1-1'
# train_end_date = '2023-1-1'
train_start_date = '2022-6-11'
train_end_date = '2022-8-11'

test_start_date = '2022-6-11'
test_end_date = '2022-9-2'
baseline_ticker = 'AXP'

model_name = 'ppo'
MODEL_IDX = f'{model_name}_{train_start_date}_{train_end_date}'
MODEL_IDX = 'ppo_2022-6-11_2022-8-11_2023-3-4-0-10-6'


def train_and_test(
        train_start_date,
        train_end_date,
        test_start_date,
        test_end_date,
        ticker_list,
        candle_time_interval,
        baseline_ticker,
        model_name,
        MODEL_IDX,
        to_train=False,
        erl_params=None,
):  
    if to_train:
        if erl_params is None:
            curr_params = ERL_PARAMS
        else:
            curr_params = erl_params
        
        train(start_date=train_start_date,
            end_date=train_end_date,
            ticker_list=ticker_list,
            data_source='alpaca',
            time_interval=candle_time_interval,
            technical_indicator_list=INDICATORS,
            drl_lib='elegantrl',
            #       drl_lib='rllib',
            #       drl_lib='stable_baselines3',
            env=env,
            model_name=model_name,
            API_KEY=API_KEY,
            API_SECRET=API_SECRET,
            API_BASE_URL=API_BASE_URL,
            erl_params=curr_params,
            cwd=f'./log/{MODEL_IDX}',  # current_working_dir
            wandb=False,
            break_step=1e7)

    account_value = test(start_date=test_start_date,
                         end_date=test_end_date,
                         ticker_list=ticker_list,
                         data_source='alpaca',
                         time_interval=candle_time_interval,
                         technical_indicator_list=INDICATORS,
                         drl_lib='elegantrl',
                         env=env,
                         model_name='ppo',
                         API_KEY=API_KEY,
                         API_SECRET=API_SECRET,
                         API_BASE_URL=API_BASE_URL,
                         #       erl_params=ERL_PARAMS,
                         cwd=f'./log/{MODEL_IDX}',  # current_working_dir
                         if_plot=True,  # to return a dataframe for backtest_plot
                         break_step=1e7)
    print("============== account_value ===========")
    print(account_value)

    # baseline stats
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline_v2(            
            ticker = baseline_ticker, 
            start = test_start_date,
            end = test_end_date)

    stats = backtest_stats(baseline_df, value_col_name='close')
    print(stats)

    print("==============Compare to Baseline===========")
    figs, returns = backtest_plot_v2(account_value, baseline_df)
    figs.savefig(f'./log/{MODEL_IDX}/backtest.pdf')
    return returns.sum()



if __name__ == '__main__':
    train_and_test(train_start_date, train_end_date, test_start_date, test_end_date, ticker_list, candle_time_interval, 
    baseline_ticker, model_name, MODEL_IDX, )
