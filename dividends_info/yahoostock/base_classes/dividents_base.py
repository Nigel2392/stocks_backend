import datetime

class DividentsBase:
    def get_dividend_change_over_years(self, dividends, years, end_date):
        recent_dividend_rate = self.get_yearly_dividend_rate_from_date(dividends, end_date)
        days_ago = years * 365
        years_back_datetime = end_date - datetime.timedelta(days=days_ago)
        years_back_dividend_rate = self.get_yearly_dividend_rate_from_date(dividends, years_back_datetime)

        if not years_back_dividend_rate:
            return "there was no dividend back then"

        # print("recent dividend rate is %s" % recent_dividend_rate)
        # print("years_back_dividend_rate rate is %s" % years_back_dividend_rate)

        increase = round(((recent_dividend_rate - years_back_dividend_rate) / years_back_dividend_rate * 100 / years), 1)
        # print("{years} year increase is: {increase}%".format(years=years, increase=increase))
        return increase

    def retrieve_dividend_change_over_time(self, dividends, years_back_list):
        today = datetime.date.today()
        yield_changes = {}
        for years_back in years_back_list:
            change = self.get_dividend_change_over_years(dividends, years_back, today)
            key = 'dividend_change_' + str(years_back) + '_year'
            yield_changes[key] = change
        return yield_changes

    def get_current_dividend_yield(self, price, dividends):
        """TODO: make this take a start and end date so you can get the yield from any period

         this doesnt need any dates because current assumes were checking the rate over this past year"""
        rate = self.get_yearly_dividend_rate_from_date(dividends, datetime.date.today())
        return round((rate / price) * 100, 2)

    def retrieve_dividend_change_over_time(self, dividends, years_back_list):
        today = datetime.date.today()
        yield_changes = {}
        for years_back in years_back_list:
            change = self.get_dividend_change_over_years(dividends, years_back, today)
            key = 'dividend_change_' + str(years_back) + '_year'
            yield_changes[key] = change
        return yield_changes

    def get_yearly_dividend_rate_from_date(self, dividends, target_date):
        one_year_previous_datetime = target_date - datetime.timedelta(days=365)
        dividends_within_one_year_previous_of_target_date = self.get_dividends_within_time_span(dividends, one_year_previous_datetime, target_date)
        yearly_dividend_rate = 0
        # print("totaling dividends for the dividend rate:")
        for dividend in dividends_within_one_year_previous_of_target_date:
            # print("date: {date}, amount: {amount}".format(date=dividend['date'], amount=dividend['amount']))
            yearly_dividend_rate += dividend['amount']
        return round(yearly_dividend_rate, 2)

    def retrieve_dividends_going_back_n_years(self, dividends, years_back):
        today = datetime.date.today()
        days_ago = years_back * 365
        years_back_datetime = today - datetime.timedelta(days=days_ago)
        dividends_over_certain_year_timespan = self.get_dividends_within_time_span(dividends, years_back_datetime, today)
        formatted_dividends_data = self.dividends_datetime_to_string(dividends_over_certain_year_timespan)
        return formatted_dividends_data

    @staticmethod
    def get_dividends_within_time_span(dividends, start_date, end_date):
        """change to take a time span of start, end, 2 dates and grab dividends within those dates"""
        dividends_within_one_year_of_years_ago = []
        for dividend in dividends:
            if dividend['date'] >= start_date and dividend['date'] <= end_date:
                dividends_within_one_year_of_years_ago.append(dividend)
        return dividends_within_one_year_of_years_ago

    @staticmethod
    def dividends_datetime_to_string(data):
        str_data = []
        for dict in data:
            str_data.append({'date': dict['date'].strftime("%m/%d/%Y"), 'amount': dict['amount']})
        return str_data
