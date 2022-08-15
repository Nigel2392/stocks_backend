import datetime

from djongo import models


class Dividend(models.Model):
    date = models.DateField()
    amount = models.FloatField()

    class Meta:
        abstract = True


class StockInfo(models.Model):
    ticker = models.CharField(max_length=100)
    current_price = models.FloatField()
    name = models.CharField(max_length=255)
    summary = models.TextField()
    sector = models.CharField(max_length=100)
    dividends = models.ArrayField(model_container=Dividend)
    last_updated_time = models.DateTimeField(null=True, auto_now=True)

    objects = models.DjongoManager()

    # https://stackoverflow.com/questions/9953427/django-custom-save-model
    # def save(self, *args, **kwargs):
    #     self.last_updated_time = datetime.datetime.now().astimezone()
    #     super(StockInfo, self).save(*args, **kwargs)
