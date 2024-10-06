from django.db import models


class Parsanalyze(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=True, default='')
    book_price = models.CharField(max_length=100, blank=True, default='')
    curr_price = models.CharField(max_length=100, blank=True, default='')
    sfrw_price = models.CharField(max_length=100, blank=True, default='')
    lfrw_price = models.CharField(max_length=100, blank=True, default='')


class BestForBuying(models.Model):
    full_title = models.CharField(max_length=100, blank=True, default='')
    short_title = models.CharField(max_length=100, unique=True, blank=True, default='')
