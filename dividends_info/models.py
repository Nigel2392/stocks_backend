# from django.db import models

from djongo import models


class Dividend(models.Model):
    date = models.CharField(max_length=40)
    amount = models.FloatField()

    class Meta:
        abstract = True

class StockInfo(models.Model):
    ticker = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    description = models.TextField()
    sector = models.CharField(max_length=100)
    dividends = models.ArrayField(model_container=Dividend)
