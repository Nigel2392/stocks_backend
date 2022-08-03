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
    get_dividends_within_time_span,
    get_yearly_dividend_rate_from_date,
)

# HOW TO RETURN JSON
# https://stackoverflow.com/questions/9262278/how-do-i-return-json-without-using-a-template-in-django

def get_dividends(ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    dividends = get_all_dividends(yahoo_stock_obj)
    return dividends


def dividends_datetime_to_string(data):
    str_data = []
    for dict in data:
        str_data.append({'date': dict['date'].strftime("%m/%d/%Y"), 'amount': dict['amount']})
    return str_data


def main_dividends_results(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())

    current_price = get_current_price(yahoo_stock_obj)

    dividends_data = {
        'current_price': current_price,
    }
    json_data = json.dumps(dividends_data)
    return HttpResponse(json_data, content_type='application/json')


def current_price_view(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    current_price = get_current_price(yahoo_stock_obj)
    current_price_object = {'current_price': current_price}
    data = json.dumps(current_price_object)
    return HttpResponse(data, content_type='application/json')



def get_dividend_yield_change_for_certain_years_ago_view(request, ticker, years_ago):
    dividends = get_dividends(ticker)
    today = datetime.date.today()
    change = get_dividend_change_over_years(dividends, years_ago, today)
    change_object = {'change': change}
    data = json.dumps(change_object)
    return HttpResponse(data, content_type='application/json')


def current_dividend_yield_view(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    # import ipdb; ipdb.set_trace()
    price = get_current_price(yahoo_stock_obj)
    dividends = get_all_dividends(yahoo_stock_obj)
    current_yield = get_current_dividend_yield(price, dividends)
    current_yield_object = {'current_yield': current_yield}
    data = json.dumps(current_yield_object)
    return HttpResponse(data, content_type='application/json')


def dividends_over_last_certain_years(request, ticker, years_back):
    dividends = get_dividends(ticker)
    today = datetime.date.today()
    days_ago = years_back * 365
    years_back_datetime = today - datetime.timedelta(days=days_ago)
    dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
    formatted_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
    data = json.dumps(formatted_data)
    return HttpResponse(data, content_type='application/json')


def recent_yearly_dividend_rate(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    dividends = get_all_dividends_dicts(yahoo_stock_obj)
    print("dividends")
    print(dividends)
    # import ipdb; ipdb.set_trace()
    today = datetime.date.today()
    rate = get_yearly_dividend_rate_from_date(dividends, today)
    rate_object = {'year_dividend_rate': rate}
    data = json.dumps(rate_object)
    return HttpResponse(data, content_type='application/json')
