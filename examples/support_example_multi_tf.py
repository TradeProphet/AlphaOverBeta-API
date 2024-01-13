import logging
import os
from pathlib import Path

import yfinance as yf
from Clients.Python.AOB_API import Support
import mplfinance as mpf


logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_support(quotes, support ,name, img_folder):
    hlines = list(support.keys())#[k for k in support.keys() if support[k] > 2]
    apds = []
    mpf.plot(quotes, style='charles', type='candlestick', figsize=(16, 8), title=name,
             warn_too_much_data=len(quotes) + 1, returnfig=True, savefig=os.path.join(img_folder, '{}_sr.png'.format(name)),
             show_nontrading=False, addplot=apds,
             volume=True, hlines=dict(hlines=hlines, colors=['g'], linewidths=(1.5), linestyle='--'))


def top_support(support_d, quotes):
    support_d = {k: v for k, v in sorted(support_d.items(), key=lambda item: item[1])}
    support_lst = list(support_d.keys())[-5:]
    support_lst.sort(key=lambda x: abs(quotes['Close'].iloc[-1] - x))
    support_d = dict([(k, support_d[k]) for k in support_lst])

    return support_d


if __name__ == '__main__':
    try:
        symbol_list = Path('DOW30.txt').read_text().split('\n')
        for symbol in symbol_list:
            ticker = yf.Ticker(symbol)

            period = '3mo'
            interval = '1h'
            support_d, status_code = Support(symbol=symbol, period=period, interval=interval, key='DEMO', secret='DEMO', last=False)
            assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)
            # plot
            quotes = ticker.history(period=period, interval=interval, prepost=False)
            plot_support(quotes=quotes, support=top_support(support_d, quotes), name='{}, {}, {}'.format(symbol, period, interval), img_folder='imgs')

            period = '6mo'
            interval = '1d'
            support_d, status_code = Support(symbol=symbol, period=period, interval=interval, key='DEMO', secret='DEMO', last=False)
            assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)
            # plot
            quotes = ticker.history(period=period, interval=interval, prepost=False)
            plot_support(quotes=quotes, support=top_support(support_d, quotes), name='{}, {}, {}'.format(symbol, period, interval), img_folder='imgs')

            period = '2y'
            interval = '1wk'
            support_d, status_code = Support(symbol=symbol, period=period, interval=interval, key='DEMO', secret='DEMO', last=False)
            assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)
            # plot
            quotes = ticker.history(period=period, interval=interval, prepost=False)
            plot_support(quotes=quotes, support=top_support(support_d, quotes), name='{}, {}, {}'.format(symbol, period, interval), img_folder='imgs')

    except Exception as e:
        print(str(e))