from decouple import config
import json, requests

BASE_DARQUBE_URL = "https://api.darqube.com/"

DARQUBE_API_KEY = config('DARQUBE_API_KEY')

# https://api.darqube.com/data-api/market_data/quote/TSLA?token=your_api_key

def get_current_price_of_stock_darqube(ticker):
    
    """ TODO: use websockets- https://api.darqube.com/#operation/quote_data_api_market_data_quote__ticker__get"""

    CURRENT_PRICE_URL_END = "data-api/market_data/quote/" + ticker.upper()
    REQUEST_URL = BASE_DARQUBE_URL + CURRENT_PRICE_URL_END
    print("Request url for darqube current price lookup: {url}".format(url=REQUEST_URL))
    request_params = {'token': DARQUBE_API_KEY}
    response = requests.get(REQUEST_URL, params=request_params)
    response_unicode = response.content.decode('utf-8')
    body = json.loads(response_unicode)
    try:
        return body['price']
    except KeyError:
        return None
    except e:
        raise Exception("Unknown error getting current price of stock from darqube")
