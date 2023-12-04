import requests
import pandas as pd


class AssetGroup:
    def __init__(self, asset_group, endpoint='https://api.alphaoverbeta.net/'):
        self.endpoint = endpoint
        self.asset_group = asset_group
        self._id = None

    def signup(self, email):
        '''
        signup to the service by providing email, the API key and secret are sent to the requested email
        on initial signup only! , subsequent requests to signup with the same email are ignored
        :param email: the signup email address (for ex. home@network.com)
        :return: status code
        '''
        url = self.endpoint + '/signup?email={}'.format(email)
        r = requests.post(url=url)

        return r.status_code

    def _step(self, key, secret, params, method='POST'):
        session = requests.Session()
        session.auth = (key, secret)
        _params = ''
        for k in params.keys():
            _params += '{}={}&'.format(k, params[k])
        url = '{}/{}?{}'.format(self.endpoint, self.asset_group, _params[:-1])
        if 'POST' == method:
            r = session.post(url=url)
        else:
            r = session.get(url=url)

        return r.text, r.status_code


class WatchlistManager(AssetGroup):
    def __init__(self, endpoint):
        super().__init__(endpoint=endpoint, asset_group='watchlist')

    def watchlist_create(self,key, secret):
        '''
        create a watchlist AFTER signup , use key and secret sent in the signup email
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: watchlist id to be used later for managing the watchlist (add, remove,...)
        '''
        self._id, _ = self._step(key=key, secret=secret, params={'step':'create'})

    def watchlist_add(self, key, secret, symbol):
        '''
        add a stock to the watchlist, you must have a watchlist id created when calling watchlist create
        :param watchlist_id: the already created watchlist id
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the watchlist
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'watchlist_id':self._id, 'step':'add','symbol':symbol})

    def watchlist_remove(self, key, secret, symbol):
        '''
        remove a stock form the watchlist, you must have a watchlist id created when calling watchlist create
        :param watchlist_id: the already created watchlist id
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the watchlist
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'watchlist_id':self._id, 'step': 'remove','symbol':symbol})

    def watchlist_delete(self, key, secret):
        '''
        delete the watchlist, you must have a watchlist id created when calling watchlist create
        :param watchlist_id: the already created watchlist id, this watchlist is deleted (along with any symbols added)
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'watchlist_id':self._id, 'step': 'delete'})


    def watchlist_fetch(self, key, secret):
        '''
        fetch a watchlist with current symbol prices
        :param watchlist_id: the already created watchlist id, this watchlist is deleted (along with any symbols added)
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: a dataframe object with all symbols and their current prices
        '''
        return self._step(key=key, secret=secret, params={'watchlist_id':self._id, 'step': 'fetch'}, method='GET')


class PortfolioManager(AssetGroup):
    def __init__(self, endpoint):
        super().__init__(endpoint=endpoint, asset_group='portfolio')

    def portfolio_create(self,key, secret):
        '''
        create a portfolio AFTER signup , use key and secret sent in the signup email
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: portfolio id to be used later for managing the portfolio (add, remove,...)
        '''
        self.portfolio_id = self._step(key=key, secret=secret, params={'portfolio_id':self._id, 'step':'create'})

    def portfolio_add(self, key, secret, symbol):
        '''
        add a stock to the portfolio, you must have a portfolio id created when calling portfolio create
        :param portfolio_id: the already created portfolio id
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the portfolio
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'portfolio_id':self._id, 'step':'add','symbol':symbol})

    def portfolio_remove(self, key, secret, symbol):
        '''
        remove a stock form the portfolio, you must have a portfolio id created when calling portfolio create
        :param portfolio_id: the already created portfolio id
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the portfolio
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'portfolio_id':self._id, 'step': 'remove','symbol':symbol})

    def portfolio_delete(self, key, secret):
        '''
        delete the portfolio, you must have a portfolio id created when calling portfolio create
        :param portfolio_id: the already created portfolio id, this portfolio is deleted (along with any symbols added)
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: status code
        '''
        return self._step(key=key, secret=secret, params={'portfolio_id':self._id, 'step': 'delete'})


    def portfolio_fetch(self, key, secret):
        '''
        fetch a portfolio with current symbol prices
        :param portfolio_id: the already created portfolio id, this portfolio is deleted (along with any symbols added)
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: a dataframe object with all symbols and their current prices
        '''
        return self._step(key=key, secret=secret, params={'portfolio_id':self._id, 'step': 'fetch'})
