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
    dividends_data = {}

    current_price = get_current_price(yahoo_stock_obj)
    dividends_data['current_price'] = current_price

    dividends = get_dividends(ticker)
    today = datetime.date.today()
    yield_changes = []
    yield_years_back = [1, 3, 5, 10]
    for years_back in yield_years_back:
        change = get_dividend_change_over_years(dividends, years_back, today)
        key = 'dividend_change_' + str(years_back) + '_year'
        dividends_data[key] = change

    current_yield = get_current_dividend_yield(current_price, dividends)
    dividends_data['current_yield'] = current_yield

    rate = get_yearly_dividend_rate_from_date(dividends, today)
    dividends_data['recent_dividend_rate'] = rate

    # get dividends
    YEARS_BACK = 3
    days_ago = years_back * 365
    years_back_datetime = today - datetime.timedelta(days=days_ago)
    dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
    formatted_dividends_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
    dividends_data['all_dividends'] = formatted_dividends_data

    json_data = json.dumps(dividends_data)
    return HttpResponse(json_data, content_type='application/json')


def dividends_over_last_certain_years(request, ticker, years_back):
    dividends = get_dividends(ticker)
    today = datetime.date.today()
    days_ago = years_back * 365
    years_back_datetime = today - datetime.timedelta(days=days_ago)
    dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
    formatted_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
    data = json.dumps(formatted_data)
    return HttpResponse(data, content_type='application/json')
