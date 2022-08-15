import datetime, sys

from django.test import TestCase

from .data import DIVIDENDS_DATA_FOR_PSEC

from .functions.dividend_functions import (
    get_dividends_within_time_span,
    get_yearly_dividend_rate_from_date,
    get_dividend_change_over_years,
)

def dividends_data_string_date_to_datetime(data):
    datetime_data = []
    for dict in data:
        datetime_data.append({'date': datetime.datetime.strptime(dict['date'], "%m/%d/%Y"), 'amount': dict['amount']})
    return datetime_data

DIVIDENDS_DATA = dividends_data_string_date_to_datetime(DIVIDENDS_DATA_FOR_PSEC)


class DividendsFunctionsTests(TestCase):

    # https://stackoverflow.com/questions/5917587/django-unit-tests-without-a-db
    databases = []

    def test_get_dividends_within_time_span_1(self):
        actual_dividends = get_dividends_within_time_span(DIVIDENDS_DATA, datetime.datetime(2021, 7, 25), datetime.datetime(2022, 7, 25))
        expected = [{'date': datetime.datetime(2021, 7, 27, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2021, 8, 26, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2021, 9, 27, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2021, 10, 26, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2021, 11, 24, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2021, 12, 28, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 1, 26, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 2, 23, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 3, 28, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 4, 26, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 5, 26, 0, 0), 'amount': 0.06},
                    {'date': datetime.datetime(2022, 6, 27, 0, 0), 'amount': 0.12}]
        self.assertEqual(actual_dividends, expected)

    def test_get_dividends_within_time_span_2(self):
        actual_dividends = get_dividends_within_time_span(DIVIDENDS_DATA, datetime.datetime(2019, 6, 1), datetime.datetime(2019, 12, 31))
        expected = [{'amount': 0.06, 'date': datetime.datetime(2019, 6, 27, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 7, 30, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 8, 29, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 9, 27, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 10, 30, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 11, 27, 0, 0)},
                    {'amount': 0.06, 'date': datetime.datetime(2019, 12, 31, 0, 0)}]
        self.assertEqual(actual_dividends, expected)

    def test_get_yearly_dividend_rate_from_date(self):
        actual_rate = get_yearly_dividend_rate_from_date(DIVIDENDS_DATA, datetime.datetime(2022, 7, 25))
        self.assertEqual(actual_rate, 0.78)

    def test_get_dividend_change_over_years_1(self):
        actual_change = get_dividend_change_over_years(DIVIDENDS_DATA, 10, datetime.datetime(2022, 7, 25))
        self.assertEqual(actual_change, -3.6)

    def test_get_dividend_change_over_years_2(self):
        actual_change = get_dividend_change_over_years(DIVIDENDS_DATA, 3, datetime.datetime(2022, 7, 25))
        self.assertEqual(actual_change, 2.8)
