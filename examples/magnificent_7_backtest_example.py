import sys, logging
sys.path.append('..')
from AOB_API import PortfolioManager
import ffn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


logging.getLogger('matplotlib').setLevel(logging.WARNING)


if __name__ == '__main__':
    try:
        # create the portfolio manager to manage the portfolio we backtest
        m_7_portfolio = PortfolioManager(key='DEMO', secret='DEMO')

        # create a portfolio and connect to it
        m_7_portfolio.create()

        # add symbols to the portfolio
        m_7_portfolio.add_cost(symbol='AAPL', cost=10000)
        m_7_portfolio.add_cost(symbol='MSFT', cost=10000)
        m_7_portfolio.add_cost(symbol='GOOG', cost=10000)
        m_7_portfolio.add_cost(symbol='AMZN', cost=10000)
        m_7_portfolio.add_cost(symbol='NVDA', cost=10000)
        m_7_portfolio.add_cost(symbol='META', cost=10000)
        m_7_portfolio.add_cost(symbol='TSLA', cost=10000)

        # run a backtest on the symbols added before with the requested period and the requested time interval
        m7_df, status_code = m_7_portfolio.backtest(period='5y', interval='1d')

        spy_portfolio = PortfolioManager(key='DEMO', secret='DEMO')
        spy_portfolio.create()
        spy_portfolio.add_cost(symbol='SPY', cost=10000)
        spy_df, status_code = spy_portfolio.backtest(period='5y', interval='1d')

        # print the backtest results
        bt_df = pd.DataFrame()
        bt_df['m7'] = m7_df['equity'] / m7_df['equity'].iloc[0]
        bt_df['spy'] = spy_df['equity'] / spy_df['equity'].iloc[0]
        bt_df.index = pd.to_datetime(m7_df['Date'])

        for col in bt_df.columns:
            equity = bt_df[col].iloc[1:]
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
            ax.set_title('{} Portfolio Performance (Daily)'.format(col))
            ax.get_figure().set_size_inches(wide_small_img_size)
            ax.grid(visible=True, linestyle='--')
            ax.set_ylabel(col)

            #
            # drawdown
            ax3 = plt.subplot(2, 1, 2)
            equity_dd = ffn.to_drawdown_series(f)
            ax3.plot(equity_dd.iloc[1:] * 100., color='red', linewidth=1)
            ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
            ax3.set_ylabel('Drawdown')

            plt.savefig('imgs/{}_bt_example.png'.format(col))
            plt.close()

        wide_small_img_size = (12, 8)
        bt_df['spy'] = (bt_df['spy'] - 1) * 100.
        bt_df['m7'] = (bt_df['m7'] - 1) * 100.
        ax = plt.subplot()
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title('Magnificent 7 vs SPY Performance (Daily)')
        ax.get_figure().set_size_inches(wide_small_img_size)
        ax.grid(visible=True, linestyle='--')
        bt_df.plot(figsize=wide_small_img_size, grid=True)
        ax.get_figure().savefig('imgs/SPY_M7_Performance.png')
        plt.close()

    except Exception as e:
        print(str(e))