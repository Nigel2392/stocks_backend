from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime, json, yfinance

from .functions.dividend_functions import (
    dividends_datetime_to_string,
    get_all_dividends,
    retrieve_dividend_change_over_time,
    get_current_dividend_yield,
    get_yearly_dividend_rate_from_date,
    retrieve_dividends_going_back_n_years,
    gather_dividends_data_from_yahoo_obj,
)
from.models import StockInfo

# HOW TO RETURN JSON
# https://stackoverflow.com/questions/9262278/how-do-i-return-json-without-using-a-template-in-django


def get_keys_info(yahoo_stock_obj, keys):
    info_object= yahoo_stock_obj.get_info()
    keys_info_dict = {}
    for key_dict in keys:
        try:
            keys_info_dict[key_dict['setter']] = info_object[key_dict['getter']]
        except:
            print("Couldn't find that key in yahoo get_info() object")
    return keys_info_dict


def main_dividends_results(request, ticker):
    try:
        today = datetime.date.today()
        stock = StockInfo.objects.get(ticker=ticker)
        print("found the stock")

        print("all dividends if stock does exist")
        print(stock.dividends)
        data = {}
        data['current_price'] = stock.current_price
        data['name'] = stock.name
        data['summary'] = stock.summary
        data['sector'] = stock.sector

        yield_years_back = [1, 3, 5, 10]
        changes_over_time = retrieve_dividend_change_over_time(stock.dividends, yield_years_back)
        # https://stackoverflow.com/questions/8930915/append-a-dictionary-to-a-dictionary
        data |= changes_over_time

        current_yield = get_current_dividend_yield(stock.current_price, stock.dividends)
        data['current_yield'] = current_yield

        rate = get_yearly_dividend_rate_from_date(stock.dividends, today)
        data['recent_dividend_rate'] = rate

        all_dividends_3_years_back = retrieve_dividends_going_back_n_years(stock.dividends, 3)
        # give most recent dividends in the front for display on table
        all_dividends_3_years_back.reverse()
        data['all_dividends'] = all_dividends_3_years_back

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

    except StockInfo.DoesNotExist:
        print("stock didnt exist in db")
        yahoo_stock_obj = yfinance.Ticker(ticker.upper())
        all_dividends = get_all_dividends(yahoo_stock_obj)
        data = gather_dividends_data_from_yahoo_obj(yahoo_stock_obj)
        addtional_keys = [
            {'setter': 'name', 'getter': 'longName'},
            {'setter': 'summary', 'getter': 'longBusinessSummary'},
            {'setter': 'sector', 'getter': 'sector'},
        ]
        additional_info = get_keys_info(yahoo_stock_obj, addtional_keys)
        data |= additional_info

        stock = StockInfo()
        stock.ticker = ticker
        stock.current_price = data['current_price']
        stock.name = data['name']
        stock.summary = data['summary']
        try:
            stock.sector = data['sector']
        except:
            stock.sector = ''
        print("all dividends if stock didnt exist")
        print(all_dividends)
        # all_dividends_with_datestrings = dividends_datetime_to_string(all_dividends)
        stock.dividends = all_dividends
        stock.save()

        print(data)
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
