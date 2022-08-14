from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from helpers.view_functions import parse_request_body
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
        body = parse_request_body(request)
        searches = body['searches']
        searches_objects = [{'search_term': x} for x in searches]
        print("New searches for user {user_id}".format(user_id=user_id))
        print(searches_objects)
        user = UserProfile.objects.get(user_id=user_id)
        user.searches = searches_objects
        user.save()
        return HttpResponse("it worked")
