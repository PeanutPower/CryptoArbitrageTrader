
import time
import httplib
import urllib
import json
import hashlib
import hmac


class API():
    """ This is an implementation of the BTC-e private trade API and the public
information API.
Please refer to https://btc-e.com/api/documentation for API
documentation.
"""

    def __init__(self, key, secret, nonce=''):
        """ Initialize the API with your API key and secret. """
        #print "Using API key: " + key
        self.key = key
        self.secret = secret
        if nonce != '':
            self.nonce = int(nonce)
        else:
            self.nonce = None
    def get_info(self):
        """ Retrieve account/API key info. """
        params = {"method":"getInfo"}
        return self._send_private(params)
    def trans_history(self, paramDict=None):
        """ Retrieve your transaction history. None of the API method
arguments are required. Pass any method arguments you want to
use as a dictionary.
Arguments:
from,count,from_id,end_id,order,since,end,pair,active
Example:
api.trans_history({"from":1341678976})
"""
        params = {"method":"TransHistory"}
        if(paramDict is not None):
            params.update(paramDict)
        return self._send_private(params)
    def trade_history(self, paramDict=None):
        """ Retrieve your trade history. None of the API method arguments are
required. Pass any method arguments you want to use as a
dictionary.
Arguments:
from,count,from_id,end_id,order,since,end,pair,active
"""
        params = {"method":"TradeHistory"}
        if(paramDict is not None):
            params.update(paramDict)
        return self._send_private(params)
    def order_list(self, paramDict=None):
        """ Retrieve your order list. None of the API method arguments are
required. Pass any method arguments you want to use as a
dictionary.
Arguments:
from,count,from_id,end_id,order,since,end,pair
"""
        params = {"method":"OrderList"}
        if(paramDict is not None):
            params.update(paramDict)
        return self._send_private(params)
    def trade(self, buySell, amount, pair, rate):
        """ Execute a trade to the argument pair. """
        params = {"method":"Trade",
                  "pair":pair,
                  "type":buySell,
                  "rate":rate,
                  "amount":amount}
        return self._send_private(params)
    def cancel_order(self, orderId):
        """ Cancel the argument order """
        params = {"method":"CancelOrder",
                  "order_id":orderId}
        return self._send_private(params)
    def ticker(self, pair):
        """Retrieve argument pair ticker. Pairs are in ltc_btc format."""
        return self._send_public(pair, "ticker")
    def trades(self, pair):
        """Retrieve argument pair trades. Pairs are in ltc_btc format."""
        return self._send_public(pair, "trades")
    def depth(self, pair):
        """Retrieve market depth for argument pair.
Pairs are in ltc_btc format."""
        return self._send_public(pair, "depth")
    def _send_private(self, params):
        """ Send a request to the private API using your API key and secret."""
        try:
            params.update(nonce=self._get_nonce())
            params = urllib.urlencode(params)
            crypto = hmac.new(self.secret, params, hashlib.sha512)
            sign = crypto.hexdigest()
            header = self._get_header(sign)
            conn = httplib.HTTPSConnection("btc-e.com")
            conn.request("POST", "/tapi", params, header)
            response = conn.getresponse()
            try:
                response = json.load(response)
            except ValueError:
                response = {'success':0, 'error':'No JSON in response. BTC-e down.'}
            conn.close()
            return response
        except:
            return {'success':0, 'error':'Connection failed.'}
    def _get_header(self, sign):
        """ Get a header for private API with the sign header
set as sign argument.
"""
        return {"Content-type": "application/x-www-form-urlencoded",
                "Key":self.key,
                "Sign":sign}
    def _send_public(self, pair, method):
        """ Send a request to the public API """
        try:
            conn = httplib.HTTPSConnection("btc-e.com")
            url = "/api/2/" + pair + "/" + method
            conn.request("GET", url)
            response = conn.getresponse()
            try:
                response = json.load(response)
            except ValueError:
                response = {'success':0, 'error':'No JSON in response. BTC-e down.'}
            conn.close()
            return response
        except:
            return {'success':0, 'error':'Connection failed.'}
    def _get_nonce(self):
        """ Generate a nonce. """
        if self.nonce is not None:
            self.nonce = self.nonce + 1
        else:
            self.nonce = 1
        return self.nonce
