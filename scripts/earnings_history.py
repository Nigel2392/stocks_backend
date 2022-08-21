import yfinance

yahoo_stock_obj = yfinance.Ticker('HD'.upper())

info = yahoo_stock_obj.get_info()

# history = yahoo_stock_obj.earnings_history
#
# print(history)
#
# print(history.iloc[0])
#
# print("\n\n")
#
# print(history.iloc[0][4])
#
# print(history["Symbol"])

def gather_earnings_objects(yahoo_obj):
    history = yahoo_obj.earnings_history
    row_count = 100
    earnings = []
    for i in range(row_count):
        print(i)
        data = {}
        data['date'] = history.iloc[i][2]
        data['expected'] = history.iloc[i][3]
        data['actual'] = history.iloc[i][4]
        data['surprise'] = history.iloc[i][5]
        earnings.append(data)
    print(earnings)
    return earnings

gather_earnings_objects(yahoo_stock_obj)
# import ipdb; ipdb.set_trace()
