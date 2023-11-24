import requests
import pandas as pd


def signup(email):
    '''
    signup to the service by providing email, the API key and secret are sent to the requested email
    on initial signup only! , subsequent requests to signup with the same email are ignored
    :param email: the signup email address (for ex. home@network.com)
    :return: status code
    '''
    url = 'https://api.alphaoverbeta.net/signup?email={}'.format(email)
    r = requests.post(url=url)

    return r.status_code


def watchlist_create(key, secret):
    '''
    create a watchlist AFTER signup , use key and secret sent in the signup email
    :param key: the key string sent after signup
    :param secret: the secret string sent after signup
    :return: watchlist id to be used later for managing the watchlist (add, remove,...)
    '''
    session = requests.Session()
    session.auth = (key, secret)
    url = 'https://api.alphaoverbetaa.net/watchlist?action=create'
    r = session.post(url=url)
    wid = r.text

    return wid


def watchlist_add(watchlist_id, key, secret, symbol):
    '''
    add a stock to the watchlist, you must have a watchlist id created when calling watchlist create
    :param watchlist_id: the already created watchlist id
    :param key: the key string sent after signup
    :param secret: the secret string sent after signup
    :param symbol: the symbol to add to the watchlist
    :return: status code
    '''
    session = requests.Session()
    session.auth = (key, secret)
    url = 'https://api.alphaoverbetaa.net/watchlist?watchlist_id={}&action=add&symbol={}'.format(watchlist_id, symbol)
    r = session.post(url=url)

    return r.status_code


def watchlist_remove(watchlist_id, key, secret, symbol):
    '''
    remove a stock form the watchlist, you must have a watchlist id created when calling watchlist create
    :param watchlist_id: the already created watchlist id
    :param key: the key string sent after signup
    :param secret: the secret string sent after signup
    :param symbol: the symbol to add to the watchlist
    :return: status code
    '''
    session = requests.Session()
    session.auth = (key, secret)
    url = 'https://api.alphaoverbetaa.net/watchlist?watchlist_id={}&action=remove&symbol={}'.format(watchlist_id, symbol)
    r = session.post(url=url)

    return r.status_code


def watchlist_delete(watchlist_id, key, secret):
    '''
    delete the watchlist, you must have a watchlist id created when calling watchlist create
    :param watchlist_id: the already created watchlist id, this watchlist is deleted (along with any symbols added)
    :param key: the key string sent after signup
    :param secret: the secret string sent after signup
    :return: status code
    '''
    session = requests.Session()
    session.auth = (key, secret)
    url = 'https://api.alphaoverbetaa.net/watchlist?watchlist_id={}&action=delete'.format(watchlist_id)
    r = session.post(url=url)

    return r.status_code


def watchlist_fetch(watchlist_id, key, secret):
    '''
    fetch a watchlist with current symbol prices
    :param watchlist_id: the already created watchlist id, this watchlist is deleted (along with any symbols added)
    :param key: the key string sent after signup
    :param secret: the secret string sent after signup
    :return: a dataframe object with all symbols and their current prices
    '''
    session = requests.Session()
    session.auth = (key, secret)
    url = 'https://api.alphaoverbetaa.net/watchlist?watchlist_id={}&action=fetch'.format(watchlist_id)
    wlj = session.get(url=url)
    df = pd.DataFrame(wlj.json())

    return df
