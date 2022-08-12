# from django.db import models

from djongo import models


class RecentSearch(models.Model):
    search_term = models.CharField(max_length=100)

    class Meta:
        abstract = True

class UserProfile(models.Model):
    user_id = models.CharField(max_length=255)
    searches = models.ArrayField(model_container=RecentSearch)
