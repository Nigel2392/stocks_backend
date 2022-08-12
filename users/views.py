from django.shortcuts import render
from django.http import HttpResponse

from .models import UserProfile
# from utils import get_db_handle

# handle, db_client =

def main_user_profile(request, user_id):
    # yahoo_stock_obj = yfinance.Ticker(ticker.upper())
    # data = gather_dividends_data(yahoo_stock_obj)
    # addtional_keys = [
    #     {'setter': 'name', 'getter': 'longName'},
    #     {'setter': 'summary', 'getter': 'longBusinessSummary'},
    #     {'setter': 'sector', 'getter': 'sector'},
    # ]
    # additional_info = get_keys_info(yahoo_stock_obj, addtional_keys)
    # data |= additional_info
    # json_data = json.dumps(data)
    # return HttpResponse(json_data, content_type='application/json')
    try:
        user = UserProfile.objects.get(user_id=user_id)
    except:
        user = None
    print(user)
    return HttpResponse("user id {user_id}".format(user_id=user_id))
