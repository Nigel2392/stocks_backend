from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime, json, yfinance

from .functions import (
    get_all_dividends,
    get_current_price,
    get_dividend_change_over_years,
    get_current_dividend_yield,
    get_all_dividends_dicts,
)

# HOW TO RETURN JSON
# https://stackoverflow.com/questions/9262278/how-do-i-return-json-without-using-a-template-in-django


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_dividend_yield_change_for_certain_years_ago_view(request, ticker, years_ago):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    dividends = get_all_dividends(yahoo_stock_obj)
    today = datetime.date.today()
    change = get_dividend_change_over_years(dividends, years_ago, today)
    change_object = {'change': change}
    data = json.dumps(change_object)
    return HttpResponse(data, content_type='application/json')


def current_dividend_yield_view(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    get_all_dividends_dicts(yahoo_stock_obj)
    # print(get_all_dividends(yahoo_stock_obj))
    price = get_current_price(yahoo_stock_obj)
    dividends = get_all_dividends(yahoo_stock_obj)
    current_yield = get_current_dividend_yield(price, dividends)
    current_yield_object = {'current_yield': current_yield}
    data = json.dumps(current_yield_object)
    return HttpResponse(data, content_type='application/json')
