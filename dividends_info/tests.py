import datetime, sys

from django.test import TestCase

from .data import DIVIDENDS_DATA_FOR_PSEC

from .functions import (
    get_dividends_within_time_span,
)

def dividends_data_string_date_to_datetime(data):
    datetime_data = []
    for dict in data:
        datetime_data.append({'date': datetime.datetime.strptime(dict['date'], "%m/%d/%Y"), 'amount': dict['amount']})
    return datetime_data

class DividendsFunctionsTests(TestCase):

    def test_get_dividends_within_time_span_1(self):
        dividends_data = dividends_data_string_date_to_datetime(DIVIDENDS_DATA_FOR_PSEC)
        actual_dividends = get_dividends_within_time_span(dividends_data, datetime.datetime(2021, 7, 25), datetime.datetime(2022, 7, 25))
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
