from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime, json, yfinance

from .functions.dividend_functions import (
    dividends_datetime_to_string,
    get_all_dividends,
    get_current_price,
    get_dividend_change_over_years,
    get_current_dividend_yield,
    get_all_dividends_dicts,
    get_dividends_within_time_span,
    get_yearly_dividend_rate_from_date,
    retrieve_dividend_change_over_time,
    retrieve_dividends_going_back_n_years,
)

# HOW TO RETURN JSON
# https://stackoverflow.com/questions/9262278/how-do-i-return-json-without-using-a-template-in-django

# def get_dividends(ticker):
#     yahoo_stock_obj = yfinance.Ticker(ticker.upper())
#     dividends = get_all_dividends(yahoo_stock_obj)
#     return dividends


def main_dividends_results(request, ticker):
    yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    dividends = get_all_dividends(yahoo_stock_obj)
    today = datetime.date.today()
    dividends_data = {}

    current_price = get_current_price(yahoo_stock_obj)
    dividends_data['current_price'] = current_price

    yield_years_back = [1, 3, 5, 10]
    changes_over_time = retrieve_dividend_change_over_time(dividends, yield_years_back)
    dividends_data |= changes_over_time

    current_yield = get_current_dividend_yield(current_price, dividends)
    dividends_data['current_yield'] = current_yield

    rate = get_yearly_dividend_rate_from_date(dividends, today)
    dividends_data['recent_dividend_rate'] = rate

    # get dividends
    # YEARS_BACK = 3
    all_dividends_3_years_back = retrieve_dividends_going_back_n_years(dividends, 3)
    # days_ago = YEARS_BACK * 365
    # years_back_datetime = today - datetime.timedelta(days=days_ago)
    # dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
    # formatted_dividends_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
    dividends_data['all_dividends'] = all_dividends_3_years_back

    json_data = json.dumps(dividends_data)
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
