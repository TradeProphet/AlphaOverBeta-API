import sys, logging
from pathlib import Path
from numpy import arange

sys.path.append('..')
from AOB_API import PortfolioManager
import ffn
import pandas as pd

logging.getLogger('matplotlib').setLevel(logging.WARNING)


if __name__ == '__main__':
    Path('imgs').mkdir(parents=True, exist_ok=True)
    perf_df = pd.DataFrame()
    try:
        # create the portfolio manager to manage the portfolio we backtest
        portfolio_api = PortfolioManager(key='DEMO', secret='DEMO')

        # initial portfolio size in $ terms is $20K
        portfolio_size = 20000

        # iterate over all portfolio combinations of SH and SPY
        for equity_size_p in arange(0.1,1,0.1):
            # calculate the cost to buy SH and SPY
            equity_cost = equity_size_p * portfolio_size

            sh_cost = portfolio_size - equity_cost
            # create a portfolio and connect to it
            portfolio_api.create()

            # add symbols to the portfolio
            portfolio_api.add_cost(symbol='SPY', cost=equity_cost)
            portfolio_api.add_cost(symbol='SH', cost=sh_cost)

            # run a backtest on the symbols added before with the requested period and the requested time interval
            bt_df, status_code = portfolio_api.backtest(period='3y', interval='1d')
            perf_df['SPY {:.1f}%, SH {:.1f}%'.format(100.*equity_size_p, 100.*(1-equity_size_p))] = bt_df['equity'] / bt_df['equity'].iloc[0]
            portfolio_api.delete()

            # print the backtest results
            bt_df.index = pd.to_datetime(bt_df['Date'])
            equity = bt_df['equity'].iloc[1:]
            stats = equity.calc_stats()
            print('Backtest results ({} : {}):\n\tTotal Return:{:.2f}%\n\tSharpe:{:.2f}\n\tMaximum Drawdown:{:.2f}%'.format(stats.start.date(), stats.end.date(), 100.*stats.incep, stats.monthly_sharpe, 100.*stats.max_drawdown))

        # plot results
        wide_small_img_size = (12, 8)
        perf_df.index = bt_df.index
        perf_df.plot(figsize=wide_small_img_size, grid=True).get_figure().savefig('imgs/SPY_SH_Performance.png')

    except Exception as e:
        print(str(e))