from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import UserProfile

@csrf_exempt
def get_user_profile(request, user_id):
    if request.method == 'GET':
        try:
            user = UserProfile.objects.get(user_id=user_id)
            print("user found")
        except Exception as error:
            print("User profile wasnt found:")
            print(error)
            user = None
            profile = UserProfile()
            profile.user_id = user_id
            profile.searches = [
                {'search_term': 'hd'},
                {'search_term': 'wba'},
            ]
            profile.save()
            print("user saved in db")
            user = UserProfile.objects.get(user_id=user_id)

        data = {
            'user_id': user.user_id,
            'searches': user.searches
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    if request.method == 'POST':
        data = request.POST
        print(data)
        print(data.keys())
        return HttpResponse("it worked")


# def update_user_profile(request, user_id):
#     try:
#         user = UserProfile.objects.get(user_id=user_id)
#         print("user found")
#     except:
#         user = None
#         profile = UserProfile()
#         profile.user_id = user_id
#         profile.searches = [
#             {'search_term': 'hd'},
#             {'search_term': 'wba'},
#         ]
#         profile.save()
#         print("user saved in db")
#         user = UserProfile.objects.get(user_id=user_id)
#
#     data = {
#         'user_id': user.user_id,
#         'searches': user.searches
#     }
#     json_data = json.dumps(data)
#     return HttpResponse(json_data, content_type='application/json')
