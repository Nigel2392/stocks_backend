import datetime


def get_current_price(yahoo_obj):
    info = yahoo_obj.get_info()
    price = info['currentPrice']
    return price


def get_all_dividends(yahoo_obj):
    panda_dividends_obj = yahoo_obj.dividends
    dividends_dicts = []
    for i, v in panda_dividends_obj.iteritems():
        dividends_dicts.append({'date': i.to_pydatetime().date(), 'amount': v})
    return dividends_dicts


def get_all_dividends_dicts(yahoo_obj):
    panda_dividends_obj = yahoo_obj.dividends
    dividends_dicts = []
    for i, v in panda_dividends_obj.iteritems():
        dividends_dicts.append({'date': i.to_pydatetime().date(), 'amount': v})
    final_dicts = []
    for dict in dividends_dicts:
        final_dicts.append({'date': dict['date'].strftime("%m/%d/%Y"), 'amount': dict['amount']})
    print(final_dicts)


# TESTED
def get_dividends_within_time_span(dividends, start_date, end_date):
    """change to take a time span of start, end, 2 dates and grab dividends within those dates"""
    dividends_within_one_year_of_years_ago = []
    for dividend in dividends:
        if dividend['date'] >= start_date and dividend['date'] <= end_date:
            dividends_within_one_year_of_years_ago.append(dividend)
    return dividends_within_one_year_of_years_ago


# TESTED
def get_yearly_dividend_rate_from_date(dividends, target_date):
    one_year_previous_datetime = target_date - datetime.timedelta(days=365)
    dividends_within_one_year_previous_of_target_date = get_dividends_within_time_span(dividends, one_year_previous_datetime, target_date)
    yearly_dividend_rate = 0
    print("totaling dividends for the dividend rate:")
    for dividend in dividends_within_one_year_previous_of_target_date:
        print("date: {date}, amount: {amount}".format(date=dividend['date'], amount=dividend['amount']))
        yearly_dividend_rate += dividend['amount']
    return round(yearly_dividend_rate, 2)


def get_dividend_change_over_years(dividends, years, end_date):
    recent_dividend_rate = get_yearly_dividend_rate_from_date(dividends, end_date)
    days_ago = years * 365
    years_back_datetime = end_date - datetime.timedelta(days=days_ago)
    years_back_dividend_rate = get_yearly_dividend_rate_from_date(dividends, years_back_datetime)

    print("recent dividend rate is %s" % recent_dividend_rate)
    print("years_back_dividend_rate rate is %s" % years_back_dividend_rate)

    increase = round(((recent_dividend_rate - years_back_dividend_rate) / years_back_dividend_rate * 100 / years), 1)
    print("{years} year increase is: {increase}%".format(years=years, increase=increase))
    return increase


def get_current_dividend_yield(price, dividends):
    """ this doesnt need any dates because current assumes were checking the rate over this past year"""
    rate = get_yearly_dividend_rate_from_date(dividends, datetime.date.today())
    return round((rate / price) * 100, 2)
