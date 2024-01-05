import json
import logging
import yfinance as yf
from Clients.Python.AOB_API import Support
import mplfinance as mpf

logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_stock_data(name, quotes, support, last):
    hlines = [float(k) for k in support.keys() if support[k] > 2]
    apds = [
        mpf.make_addplot([last] * len(quotes), color='green', ylabel='Current', width=1.8, secondary_y=False, panel=0),
    ]
    mpf.plot(quotes, style='charles', type='candlestick', figsize=(16, 8), title=name,
             warn_too_much_data=len(quotes) + 1, returnfig=True, savefig='imgs/{}_sr.png'.format(name),
             show_nontrading=False, addplot=apds,
             volume=True, hlines=dict(hlines=hlines, colors=['g'], linewidths=(0.5), linestyle='--'))


if __name__ == '__main__':
    try:
        # use the support api to calculate the entire support areas for the requested period
        # the return value is a dictionary indicating the strength of each support level
        symbol = 'SPY'
        support_d, status_code = Support(symbol=symbol, period='1y', interval='1d', key='DEMO', secret='DEMO', last=False)
        assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)

        # use the support api to calculate the most relevant support area for the requested period
        # the return value is a dictionary indicating the strength of the current support level
        symbol = 'SPY'
        current_support, status_code = Support(symbol=symbol, period='1y', interval='1d', key='DEMO', secret='DEMO', last=True)
        assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)

        # plot
        ticker = yf.Ticker(symbol)
        quotes = ticker.history(period='1y', interval="1d", prepost=False)
        plot_stock_data(quotes=quotes, support=support_d, name=symbol, last=current_support)

    except Exception as e:
        print(str(e))