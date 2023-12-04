import requests

'''
an asset group is the interface class for any group of assets (watchlist, portfolio,...)
'''
class AssetGroup:
    def __init__(self, asset_group, endpoint='https://api.alphaoverbeta.net/'):
        '''
        initialize the asset group
        :param asset_group: string representing the group of assets 'must be the same as the one in the backend
        :param endpoint: url of endpoint, may be local (testing) alphaoverbeta is the default
        '''
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
        '''
        internal method executing the request to the backend
        :param key: the key string
        :param secret: the secret string
        :param params: dictionary containing the values for the endpoint params
        :param method: POST,GET
        :return: response string and status code (must be 200 for succesfull requests)
        '''
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

    def create(self,key, secret):
        '''
        create an asset group AFTER signup , use key and secret sent in the signup email
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: id to be used later for managing the watchlist (add, remove,...)
        '''
        self._id, _ = self._step(key=key, secret=secret, params={'step':'create'})

    def add(self, key, secret, symbol, kwargs=None):
        '''
        add a stock to the group, you must have an id created when calling create
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the watchlist
        :return: status code
        '''
        assert self._id is not None
        params = {'id': self._id, 'step': 'add', 'symbol': symbol}
        if kwargs is not None:
            params.update(kwargs)
        return self._step(key=key, secret=secret, params=params)

    def remove(self, key, secret, symbol):
        '''
        remove a stock form the group, you must have an id created when calling remove
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the group
        :return: status code
        '''
        assert self._id is not None
        return self._step(key=key, secret=secret, params={'id':self._id, 'step': 'remove','symbol':symbol})

    def delete(self, key, secret):
        '''
        delete the group, you must have an id created when calling delete
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: status code
        '''
        assert self._id is not None
        return self._step(key=key, secret=secret, params={'id':self._id, 'step': 'delete'})

    def fetch(self, key, secret):
        '''
        fetch a watchlist with current symbol prices
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :return: a dataframe object with all symbols and their current prices
        '''
        assert self._id is not None
        return self._step(key=key, secret=secret, params={'id':self._id, 'step': 'fetch'}, method='GET')


'''
managing a watchlist
'''
class WatchlistManager(AssetGroup):
    def __init__(self, endpoint):
        super().__init__(endpoint=endpoint, asset_group='watchlist')

'''
managing a portfolio
'''
class PortfolioManager(AssetGroup):
    def __init__(self, endpoint):
        super().__init__(endpoint=endpoint, asset_group='portfolio')

    def add(self, key, secret, symbol, kwargs=None):
        assert False, 'quantity missing use add(...,quantity)'

    def add(self, key, secret, symbol, quantity):
        '''
        add a stock to the group, you must have an id created when calling create
        :param key: the key string sent after signup
        :param secret: the secret string sent after signup
        :param symbol: the symbol to add to the watchlist
        :return: status code
        '''
        return super().add(key=key, secret=secret, symbol=symbol, kwargs={'quantity':quantity})
