import yfinance

yahoo_stock_obj = yfinance.Ticker('HD'.upper())

keys = yahoo_stock_obj.get_info().keys()

keys_list = []

for key in keys:
    keys_list.append(key)

keys_list.sort()

print(keys_list)

with open('./info_keys.txt', 'w') as file:
    for key in keys_list:
        file.write(key)
        file.write("\n")
