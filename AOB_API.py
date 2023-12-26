import requests
import json
import pandas as pd


def signup(email, endpoint=None):
    '''
    signup to the service by providing email, the API key and secret are sent to the requested email
    on initial signup only! , subsequent requests to signup with the same email are ignored
    :param email: the signup email address (for ex. home@network.com)
    :return: status code
    '''
    endpoint = endpoint if endpoint is not None else 'https://api.alphaoverbeta.net/'
    url = endpoint + '/signup?email={}'.format(email)
    r = requests.post(url=url)

    return r.status_code


class AssetGroup:
    def __init__(self, asset_group, id, key, secret, endpoint=None):
        '''
        an asset group is the interface class for any group of assets (watchlist, portfolio,...)
        initialize the asset group
        :param asset_group: string representing the group of assets ,must be the same as the one in the backend
        :param key: the key string
        :param secret: the secret string
        :param endpoint: url of endpoint, may be local (testing), alphaoverbeta is the default
        '''
        self.endpoint = endpoint if endpoint is not None else 'https://api.alphaoverbeta.net/'
        self.asset_group = asset_group
        self._id = id
        self.key = key
        self.secret = secret

    def _step(self, params, method='POST'):
        '''
        internal method executing the request to the backend
        :param params: dictionary containing the values for the endpoint params
        :param method: POST,GET
        :return: response string and status code (must be 200 for successful requests)
        '''
        assert all([self.key, self.secret])
        session = requests.Session()
        session.auth = (self.key, self.secret)
        _params = ''
        for k in params.keys():
            _params += '{}={}&'.format(k, params[k])
        url = '{}/{}?{}'.format(self.endpoint, self.asset_group, _params[:-1])
        if 'POST' == method:
            r = session.post(url=url)
        else:
            r = session.get(url=url)

        return r.text, r.status_code

    def create(self):
        '''
        create an asset group AFTER signup , use key and secret sent in the signup email
        :return: id to be used later for managing the watchlist (add, remove,...)
        '''
        self._id, status_code = self._step(params={'step':'create'})
        if 200 != status_code:
            raise ValueError('Error creating portfolio\n, status code {}\n, id {}'.format(str(status_code), self._id))

    def add(self, symbol, kwargs=None):
        '''
        add a stock to the group, you must have an id created when calling create
        :param symbol: the symbol to add to the watchlist
        :return: status code
        '''
        assert self._id is not None, 'use create() first'
        params = {'id': self._id, 'step': 'add', 'symbol': symbol}
        if kwargs is not None:
            params.update(kwargs)
        return self._step(params=params)

    def remove(self, symbol):
        '''
        remove a stock form the group, you must have an id created when calling remove
        :param symbol: the symbol to add to the group
        :return: status code
        '''
        assert self._id is not None
        return self._step(params={'id':self._id, 'step': 'remove','symbol':symbol})

    def delete(self):
        '''
        delete the group, you must have an id created when calling delete
        :return: status code
        '''
        assert self._id is not None
        return self._step(params={'id':self._id, 'step': 'delete'})

    def fetch(self):
        '''
        fetch a group with current symbol prices
        :return: a dataframe object with all symbols and their current prices
        '''
        assert self._id is not None
        df, status_code = self._step(params={'id':self._id, 'step': 'fetch'}, method='GET')
        return pd.DataFrame(json.loads(df)), status_code


'''
managing a watchlist
'''
class WatchlistManager(AssetGroup):
    def __init__(self,key, secret, endpoint=None, id=None):
        super().__init__(endpoint=endpoint, id=id, asset_group='watchlist',key=key, secret=secret)

'''
managing a portfolio
'''
class PortfolioManager(AssetGroup):
    def __init__(self,key, secret, endpoint=None, id=None):
        super().__init__(endpoint=endpoint, id=id, asset_group='portfolio',key=key, secret=secret)

    def add(self, symbol, kwargs=None):
        assert False, 'quantity or avg_cost missing use add(...,quantity)'

    def add_quantity(self, symbol, quantity):
        '''
        add a stock to the portfolio, you must have an id created when calling create
        :param symbol: the symbol to add to the portfolio
        :param quantity: the symbol's quantity to add to the portfolio
        :return: status code
        '''
        return super().add(symbol=symbol, kwargs={'quantity':quantity})

    def add_cost(self, symbol, cost):
        '''
        add a stock to the portfolio, you must have an id created when calling create
        :param symbol: the symbol to add to the portfolio
        :param cost: the symbol's cost basis in absolute $ units, add to the portfolio
        :return: status code
        '''
        return super().add(symbol=symbol, kwargs={'cost':cost})

    def backtest(self, period, interval):
        df, status_code = self._step(params={'step':'backtest', 'id':self._id, 'period':period, 'interval':interval})
        return pd.DataFrame(json.loads(df)), status_code
