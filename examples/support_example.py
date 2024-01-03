import json, os
import sys, logging
import yfinance as yf
from Clients.Python.AOB_API import Support
sys.path.append('..')
from AOB_API import PortfolioManager
import ffn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as dates

# matplotlib.use('Agg')


logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_stock_data(name, quotes, support, resistance, maxima='', minima='', with_volume=True, ticker_open='', ticker_close=''):
    fig, ax = plt.subplots()
    # ax.plot(quotes['Close'], color='black')
    quotes['datenum'] = dates.date2num(quotes.index)
    candlestick_ohlc(ax, quotes=quotes[['datenum','Open','High','Low','Close']].values, colorup='green', colordown='firebrick')#, width=0.2)#, alpha=0.8)
    if len(maxima):
        ax.scatter(maxima.index, maxima['Close'], s=100, alpha=.5, color='firebrick', marker="v")
    if len(minima):
        ax.scatter(minima.index, minima['Close'], s=100, alpha=.5, color='green', marker="^")
    if len(ticker_open):
        ax.scatter(ticker_open.index, ticker_open, s=120, color='black', marker="^")
    if len(ticker_close):
        ax.scatter(ticker_close.index, ticker_close, s=120, color='black')  # , marker="v")
    for low in support: ax.axhline(low, color='green')  # , ls='--')
    for high in resistance: ax.axhline(high, color='red')  # , ls='--')
    ax.text(0.5, 0.5, name, transform=ax.transAxes, fontsize=50, color='gray', alpha=0.5, ha='center',
            va='center')  # https://matplotlib.org/3.2.1/gallery/text_labels_and_annotations/watermark_text.html
    if with_volume:
        ax2 = ax.twinx()
        # ax2.set_ylim(top=quotes['Volume'].max()*3)
        ax2.bar(x=quotes['Volume'].index, height=quotes['Volume'].values, alpha=0.3)  # , width=0.0001)
    plt.tight_layout()
    plt.grid(b=True, linestyle='--')
    # plt.title('{}'.format(ticker))
    fig.set_size_inches(20, 12)
    plt.savefig('./reports/' + name + '_sr.png')
    plt.close()


if __name__ == '__main__':
    try:
        symbol = 'SPY'
        support_d, status_code = Support(symbol=symbol, interval='1d', key='DEMO', secret='DEMO',endpoint='http://127.0.0.1:5000', last=False)
        assert 200 == status_code
        support_d = json.loads(support_d)

        # plot
        ticker = yf.Ticker(symbol)
        quotes = ticker.history(period="7d", interval="1m", prepost=False)
        ax = plot_stock_data(quotes=quotes, support=support_d, resistance='', name=symbol)

        # plt.show()
        plt.savefig('./reports/sr.png', dpi=300)
        os.system("start " + './reports/sr.png')

    except Exception as e:
        print(str(e))