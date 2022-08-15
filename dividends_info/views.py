from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime, json, yfinance

""" TODO: remove imported functions and write function to gather dividend data that works in both parts of the views"""
from .functions.dividend_functions import (
    get_current_price,
    # dividends_datetime_to_string,
    get_all_dividends,
    gather_dividends_data_from_dividends_array,
)
from.models import StockInfo
from .apis.api_calls import get_current_price_of_stock_darqube

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


def main_dividends_results(request, ticker, dividends_years_back):

    def get_recent_price_or_database_saved_price(ticker, stock):
        current_price = get_current_price_of_stock_darqube(ticker)
        if current_price:
            stock.current_price = current_price
            stock.save()
        else:
            current_price = stock.current_price
        return current_price

    try:
        now = datetime.datetime.now()
        today = datetime.date.today()
        stock = StockInfo.objects.get(ticker=ticker)
        print("found the stock")
        try:
            """ check if the StockInfo was updated within the last 5 minutes, if so use the db saved current price """
            print("the last updated time for stock {ticker} before save: {time}" \
                  .format(ticker=ticker, time=stock.last_updated_time.strftime("%m/%d/%Y %H:%M:%S")))

            # https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes
            the_timedelta = now - stock.last_updated_time.replace(tzinfo=None)
            print(the_timedelta)
            # https://stackoverflow.com/questions/73358271/check-if-model-was-recently-updated-fails-trying-to-use-timedelta/73360147#73360147
            if the_timedelta < datetime.timedelta(minutes=5):
                 print("stock was updated within the last 5 minutes...no need to make an api call")
                 current_price = stock.current_price
            else:
                print("stock hasn't been updated recently, make api call")
                """ TODO: use websockets- https://api.darqube.com/#operation/quote_data_api_market_data_quote__ticker__get"""
                current_price = get_recent_price_or_database_saved_price(ticker=ticker, stock=stock)

        except Exception as e:
            print("\n exception checking for last updated time: maybe the stock object didn't have a last updated time yet")
            print(e)
            """ TODO: remove duplicate code into an internal function """
            current_price = get_recent_price_or_database_saved_price(ticker=ticker, stock=stock)

        print("the last updated time for stock {ticker} after save: {time}".format(ticker=ticker, time=stock.last_updated_time.strftime("%m/%d/%Y %H:%M:%S")))

        data = {}
        data['current_price'] = current_price
        data['name'] = stock.name
        data['summary'] = stock.summary
        data['sector'] = stock.sector
        dividends_data = gather_dividends_data_from_dividends_array(
                            dividends=stock.dividends,
                            current_price=current_price,
                            yield_years_back=[1, 3, 5, 10],
                            all_dividends_years_back=dividends_years_back
                        )
        data |= dividends_data
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

    except StockInfo.DoesNotExist:
        print("stock didnt exist in db")
        yahoo_stock_obj = yfinance.Ticker(ticker.upper())
        all_dividends = get_all_dividends(yahoo_stock_obj)
        current_price = get_current_price(yahoo_stock_obj)
        data = gather_dividends_data_from_dividends_array(
                    dividends=all_dividends,
                    current_price=current_price,
                    yield_years_back=[1, 3, 5, 10],
                    all_dividends_years_back=dividends_years_back
                )
        addtional_keys = [
            {'setter': 'name', 'getter': 'longName'},
            {'setter': 'summary', 'getter': 'longBusinessSummary'},
            {'setter': 'sector', 'getter': 'sector'},
        ]
        additional_info = get_keys_info(yahoo_stock_obj, addtional_keys)
        data |= additional_info
        data['current_price'] = current_price

        stock = StockInfo()
        stock.ticker = ticker
        stock.current_price = data.get('current_price', 0)
        stock.name = data.get('name', '')
        stock.summary = data.get('summary', '')
        stock.sector = data.get('sector', '')
        stock.dividends = all_dividends
        stock.save()

        print(data)
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    except Exception as error:
        print("\nunknown error in main dividends results")
        print(error)

# def dividends_over_last_certain_years(request, ticker, years_back):
#     dividends = get_dividends(ticker)
#     today = datetime.date.today()
#     days_ago = years_back * 365
#     years_back_datetime = today - datetime.timedelta(days=days_ago)
#     dividends_over_certain_year_timespan = get_dividends_within_time_span(dividends, years_back_datetime, today)
#     formatted_data = dividends_datetime_to_string(dividends_over_certain_year_timespan)
#     data = json.dumps(formatted_data)
#     return HttpResponse(data, content_type='application/json')
