from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime, json, yfinance

from .functions.dividend_functions import gather_dividends_data

# HOW TO RETURN JSON
# https://stackoverflow.com/questions/9262278/how-do-i-return-json-without-using-a-template-in-django

# def get_dividends(ticker):
#     yahoo_stock_obj = yfinance.Ticker(ticker.upper())
#     dividends = get_all_dividends(yahoo_stock_obj)
#     return dividends

def get_keys_info(yahoo_stock_obj, keys):
    info_object= yahoo_stock_obj.get_info()
    keys_info_dict = {}
    for key in keys:
        keys_info_dict[key] = info_object[key]
    return keys_info_dict


def main_dividends_results(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    data = gather_dividends_data(yahoo_stock_obj)
    addtional_keys = ['longBusinessSummary', 'longName']
    additional_info = get_keys_info(yahoo_stock_obj, addtional_keys)
    data |= additional_info
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


# def dividends_over_last_certain_years(request, ticker, years_back):
#     dividends = get_dividends(ticker)
#     today = datetime.date.today()
#     days_ago = years_back * 365
#     years_back_datetime = today - datetime.timedelta(days=days_ago)
#     dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
#     formatted_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
#     data = json.dumps(formatted_data)
#     return HttpResponse(data, content_type='application/json')
