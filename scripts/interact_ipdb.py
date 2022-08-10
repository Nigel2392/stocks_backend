import yfinance

yahoo_stock_obj = yfinance.Ticker('HD'.upper())

info = yahoo_stock_obj.get_info()

import ipdb; ipdb.set_trace()
