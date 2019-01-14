# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_image')
    collection = models.ForeignKey(Collection, related_name='items', on_delete=models.CASCADE)
    color = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
