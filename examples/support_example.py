import json, os
import sys, logging
import yfinance as yf
from Clients.Python.AOB_API import Support
sys.path.append('..')
from AOB_API import PortfolioManager
import ffn
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_stock_data(name, quotes, support):
    hlines = [float(k) for k in support.keys() if support[k] > 2]
    mpf.plot(quotes, style='charles', type='candlestick', figsize=(16, 8), title=name,
             warn_too_much_data=len(quotes) + 1, returnfig=True, savefig='imgs/{}_sr.png'.format(name),
             show_nontrading=False,
             volume=True, hlines=dict(hlines=hlines, colors=['g'], linewidths=(0.5)))


if __name__ == '__main__':
    try:
        symbol = 'SPY'
        support_d, status_code = Support(symbol=symbol, interval='1d', key='DEMO', secret='DEMO', last=False)
        assert 200 == status_code
        support_d = json.loads(support_d)

        # plot
        ticker = yf.Ticker(symbol)
        quotes = ticker.history(period='1y', interval="1d", prepost=False)
        plot_stock_data(quotes=quotes, support=support_d, name=symbol)

    except Exception as e:
        print(str(e))