from .darqube_base import *
from .dividents_base import *
import re
import yfinance as yf

class YahooStockBase(Darqube,DividentsBase):
    TICKER = None
    YEARS = None

    def get_all_dividends(self,yahoo_obj):
        panda_dividends_obj = yahoo_obj.dividends
        dividends_dicts = []
        try:
            for i, v in panda_dividends_obj.iteritems():
                dividends_dicts.append({'date': i.to_pydatetime().date(), 'amount': v})
            return dividends_dicts
        except:
            return []

    def get_current_price(self,yahoo_obj):
        info = yahoo_obj.get_info()
        try:
            price = info['currentPrice']
        except KeyError:
            # price = info['navPrice']
            try:
                price = info['navPrice']
            except:
                price = self.get_current_price_of_stock_darqube(yahoo_obj.ticker)
        return price

    def gather_dividends_data_from_dividends_array(self,dividends, current_price, yield_years_back, all_dividends_years_back):
        today = datetime.date.today()
        data = {}

        changes_over_time = self.retrieve_dividend_change_over_time(dividends, yield_years_back)
        data |= changes_over_time

        current_yield = self.get_current_dividend_yield(current_price, dividends)
        data['current_yield'] = current_yield

        rate = self.get_yearly_dividend_rate_from_date(dividends, today)
        data['recent_dividend_rate'] = rate

        all_dividends_n_years_back = self.retrieve_dividends_going_back_n_years(dividends, all_dividends_years_back)
        # give most recent dividends in the front for display on table
        all_dividends_n_years_back.reverse()
        data['all_dividends'] = all_dividends_n_years_back

        return data

    def get_keys_info(self,yahoo_stock_obj, keys):
        info_object= yahoo_stock_obj.get_info()
        keys_info_dict = {}
        for key_dict in keys:
            try:
                keys_info_dict[key_dict['setter']] = info_object[key_dict['getter']]
            except:
                print("Couldn't find that key in yahoo get_info() object")
        return keys_info_dict

    def earnings_datetime_to_string(self,data):
        final_data = []
        for dict in data:
            final_data.append({
                'date': dict['date'].strftime("%m/%d/%Y"),
                'expected': dict['expected'],
                'actual': dict['actual'],
                'surprise': dict['surprise']
            })
        return final_data

    def gather_earnings_objects(self,yahoo_obj):
        history = yahoo_obj.earnings_history
        row_count = 100
        earnings = []
        for i in range(row_count):
            try:
                data = {}
                parsed_date = self.parse_earnings_history_date(history.iloc[i][2])
                data['date'] = parsed_date
                data['expected'] = history.iloc[i][3]
                data['actual'] = history.iloc[i][4]
                data['surprise'] = history.iloc[i][5]
                earnings.append(data)
            except IndexError:
                print("Less than 100 rows for this dataframe")
            except Exception as e:
                print(e)
                print("Unknown error parsing earnings history dataframe")
        print(earnings)
        return earnings

    def parse_earnings_history_date(self, datestring):
        regex = ".*[0-9]{4}"
        match = re.findall(regex, datestring)
        date_text = match[0]
        date = datetime.datetime.strptime(date_text, "%b %d, %Y")
        date.replace(tzinfo=None)
        return date

    def get_stock_from_yahoo(self):
        yahoo_stock_obj = yf.Ticker(self.TICKER)
        all_dividends = self.get_all_dividends(yahoo_stock_obj)
        current_price = self.get_current_price(yahoo_stock_obj)
        data = self.gather_dividends_data_from_dividends_array(
                    dividends=all_dividends,
                    current_price=current_price,
                    yield_years_back=[1, 3, 5, 10],
                    all_dividends_years_back=self.YEARS
                )
        additional_keys = [
            {'setter': 'name', 'getter': 'longName'},
            {'setter': 'summary', 'getter': 'longBusinessSummary'},
            {'setter': 'sector', 'getter': 'sector'},
        ]
        additional_info = self.get_keys_info(yahoo_stock_obj, additional_keys)
        data |= additional_info
        data['current_price'] = current_price
        earnings = self.gather_earnings_objects(yahoo_stock_obj)
        processed_earnings = self.earnings_datetime_to_string(earnings)
        data['earnings'] = processed_earnings
        return data, all_dividends, earnings



