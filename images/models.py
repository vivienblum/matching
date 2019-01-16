# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

DELTA = 25

class Collection(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ItemManager(models.Manager):
    def get_item_color(self, color, collection, delta):
        if delta == None:
            delta = 25
        return self.filter(collection=collection).filter(blue__lte=color[0] + delta ).filter(blue__gte=color[0] - delta ).filter(green__lte=color[0] + delta ).filter(green__gte=color[0] - delta ).filter(red__lte=color[0] + delta ).filter(red__gte=color[0] - delta).first()

class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_image')
    collection = models.ForeignKey(Collection, related_name='items', on_delete=models.CASCADE)
    blue = models.SmallIntegerField(null=True, blank=True)
    green = models.SmallIntegerField(null=True, blank=True)
    red = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ItemManager()

    def __str__(self):
        return self.name

class Match(object):
    def __init__(self, **kwargs):
        for field in ('image', 'collection', 'delta'):
            setattr(self, field, kwargs.get(field, None))
