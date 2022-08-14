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
        except UserProfile.DoesNotExist:
            print("user does not exist exception")
            profile = UserProfile()
            profile.user_id = user_id
            profile.searches = [
                {'search_term': 'hd'},
                {'search_term': 'wba'},
            ]
            profile.save()
            print("user saved in db")
            user = UserProfile.objects.get(user_id=user_id)
        except Exception as error:
            print("got an unknown exception:")
            print(error)

        data = {
            'user_id': user.user_id,
            'searches': user.searches
        }
        json_data = json.dumps(data)
        return HttpResponse({json_data}, content_type='application/json')

    if request.method == 'POST':
        # data = request.POST
        raw_data = request.body
        """https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django"""
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        searches = body['searches']
        searches_objects = [{'search_term': x} for x in searches]
        print(searches_objects)
        user = UserProfile.objects.get(user_id=user_id)
        user.searches = searches_objects
        user.save()
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
