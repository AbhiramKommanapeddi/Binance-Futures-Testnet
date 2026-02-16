import time
import hmac
import hashlib
import requests
import json
from .logging_config import logger

class BinanceClient:
    def __init__(self, api_key, api_secret, base_url="https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _generate_signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        timestamp = int(time.time() * 1000)
        
        if params is None:
            params = {}
        
        params['timestamp'] = timestamp
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        logger.info(f"Request: {method} {url}?{query_string}")
        
        try:
            if method == 'POST':
                response = requests.post(f"{url}?{query_string}", headers=headers)
            else:
                response = requests.get(f"{url}?{query_string}", headers=headers)
            
            response.raise_for_status()
            res_json = response.json()
            logger.info(f"Response: {json.dumps(res_json)}")
            return res_json
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error Details: {e.response.text}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, time_in_force='GTC'):
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': str(quantity)
        }
        
        if order_type.upper() == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = str(price)
            params['timeInForce'] = time_in_force
        
        if order_type.upper() == 'STOP_LIMIT':
             if price is None or stop_price is None:
                raise ValueError("Price and Stop Price are required for STOP_LIMIT orders")
             params['type'] = 'STOP'
             params['price'] = str(price)
             params['stopPrice'] = str(stop_price)
             params['timeInForce'] = time_in_force

        return self._request('POST', '/fapi/v1/order', params)

    def get_server_time(self):
        return self._request('GET', '/fapi/v1/time')
