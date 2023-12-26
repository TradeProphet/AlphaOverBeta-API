import sys, os
sys.path.append('..')
from AOB_API import PortfolioManager
import ffn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


if __name__ == '__main__':
    try:
        # create the portfolio manager to manage the portfolio we backtest
        portfolio_api = PortfolioManager(key='DEMO', secret='DEMO')

        # create a portfolio and connect to it
        portfolio_api.create()

        # add symbols to the portfolio
        portfolio_api.add_quantity(symbol='SPY', quantity=50)
        portfolio_api.add_quantity(symbol='BND', quantity=200)
        portfolio_api.add_quantity(symbol='SH', quantity=200)

        # run a backtest on the symbols added before with the requested period and the requested time interval
        bt_df, status_code = portfolio_api.backtest(period='5y', interval='1d')

        # print the backtest results
        bt_df.index = pd.to_datetime(bt_df['Date'])
        equity = bt_df['equity'].iloc[1:]
        stats = equity.calc_stats()
        stats.display()
        print('Backtest results ({} : {}):\n\tTotal Return:{:.2f}%\n\tSharpe:{:.2f}\n\tMaximum Drawdown:{:.2f}%'.format(stats.start.date(), stats.end.date(), 100.*stats.incep, stats.monthly_sharpe, 100.*stats.max_drawdown))

        # plot results
        wide_small_img_size = (12, 8)
        ax = plt.subplot(2, 1, 1)
        #
        # equity
        f = (equity / equity.iloc[0]) - 1
        ax.plot(f.iloc[1:] * 100., color='black', linewidth=1)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title('Portfolio Performance (Daily)')
        ax.get_figure().set_size_inches(wide_small_img_size)
        ax.grid(visible=True, linestyle='--')
        ax.set_ylabel('Equity')

        #
        # drawdown
        ax3 = plt.subplot(2, 1, 2)
        equity_dd = ffn.to_drawdown_series(f)
        ax3.plot(equity_dd.iloc[1:] * 100., color='red', linewidth=1)
        ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax3.set_ylabel('Drawdown')

        plt.savefig('bt_example.png')
        plt.close()

    except Exception as e:
        print(str(e))