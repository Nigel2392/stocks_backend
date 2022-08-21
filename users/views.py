from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from helpers.view_functions import parse_request_body
from .models import UserProfile

from django.db import transaction


@csrf_exempt
def get_user_profile(request, user_id):
    if request.method == 'GET':
         with transaction.atomic():
            profile, created = UserProfile.objects.get_or_create(user_id=user_id)
         if created:
             profile.user_id = user_id
             profile.searches = [
                {'search_term': 'hd'},
                {'search_term': 'wba'},
             ]
             profile.display_settings = [
                {'setting_name': 'showYieldChange', 'visible': True},
                {'setting_name': 'showAllDividends', 'visible': True},
             ]
             profile.save()
             print("user saved in db")
         user = UserProfile.objects.get(user_id=user_id)
        

        data = {
            'user_id': user.user_id,
            'searches': user.searches,
            'display_settings': user.display_settings
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
        user.display_settings = body['display_settings']
        user.save()
        return HttpResponse("it worked")
