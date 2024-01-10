import operator
import logging
import yfinance as yf
from Clients.Python.AOB_API import Support
import mplfinance as mpf

logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_support(quotes, support ,name):
    hlines = [float(k) for k in support.keys() if support[k] > 2]
    apds = []
    mpf.plot(quotes, style='charles', type='candlestick', figsize=(16, 8), title=name,
             warn_too_much_data=len(quotes) + 1, returnfig=True, savefig='{}_sr.png'.format(name),
             show_nontrading=False, addplot=apds,
             volume=True, hlines=dict(hlines=hlines, colors=['g'], linewidths=(1.5), linestyle='--'))


if __name__ == '__main__':
    try:
        # use the support api to calculate the entire support areas for the requested period
        # the return value is a dictionary indicating the strength of each support level
        symbol = 'TSLA'
        period = '3mo'
        interval = '1h'
        support_d, status_code = Support(symbol=symbol, period=period, interval=interval, key='DEMO', secret='DEMO', last=False)
        assert 200 == status_code, '[{}]\nstatus code:{}\n{}'.format(symbol, status_code, support_d)

        # find the 5 strongest support areas
        support_d = dict(sorted(support_d.items(), key=operator.itemgetter(1), reverse=True)[:5])

        # plot
        ticker = yf.Ticker(symbol)
        quotes = ticker.history(period=period, interval=interval, prepost=False)
        plot_support(quotes=quotes, support=support_d, name='{}, {}, {}'.format(symbol, period, interval))

    except Exception as e:
        print(str(e))