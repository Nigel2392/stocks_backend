from djongo import models


class RecentSearch(models.Model):
    search_term = models.CharField(max_length=100)

    class Meta:
        abstract = True


class DisplaySetting(models.Model):
    setting_name = models.CharField(max_length=150)
    visible = models.BooleanField()

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user_id = models.CharField(max_length=255)
    searches = models.ArrayField(model_container=RecentSearch, null=True)
    display_settings = models.ArrayField(model_container=DisplaySetting, null=True)

    objects = models.DjongoManager()
