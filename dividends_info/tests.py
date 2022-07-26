import datetime, sys

from django.test import TestCase

from .data import DIVIDENDS_DATA_FOR_PSEC


def dividends_data_to_datetime(data):
    datetime_data = []
    for dict in data:
        datetime_data.append({'date': datetime.datetime.strptime(dict['date'], "%m/%d/%Y"), 'amount': dict['amount']})
    return datetime_data

class DividendsFunctionsTests(TestCase):

    def test_this(self):
        data = dividends_data_to_datetime(DIVIDENDS_DATA_FOR_PSEC)
        print(data)
        # https://github.com/martinrusev/django-quick-test/issues/4
        # sys.stderr.write(repr(data) + '\n')
        # import ipdb; ipdb.set_trace()
        self.assertIs(True, False)
