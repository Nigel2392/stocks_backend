import yfinance

yahoo_stock_obj = yfinance.Ticker('HD'.upper())

info = yahoo_stock_obj.get_info()

history = yahoo_stock_obj.earnings_history

print(history)

print(history.iloc[0])

print("\n\n")

print(history.iloc[0][4])

print(history["Symbol"])

# import ipdb; ipdb.set_trace()
