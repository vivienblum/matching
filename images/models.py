# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import os

DELTA = 25

class Collection(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collections"

    def __str__(self):
        return self.name

class ItemManager(models.Manager):
    def get_item_color(self, color, collection, delta):
        if delta == None:
            delta = 25
        delta = int(delta)

        items_match = (
            self.filter(collection=collection)
            .filter(blue__lte=color[0] + delta )
            .filter(blue__gte=color[0] - delta )
            .filter(green__lte=color[1] + delta )
            .filter(green__gte=color[1] - delta )
            .filter(red__lte=color[2] + delta )
            .filter(red__gte=color[2] - delta)
        )
        # Find the closest
        best_item = None
        min = 255
        for item in items_match:
            default_blue = abs(item.blue - color[0])
            default_green = abs(item.green - color[1])
            default_red = abs(item.red - color[2])
            default = default_blue + default_green + default_red
            if default <= min:
                min = default
                best_item = item

        return best_item

class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_image')
    collection = models.ForeignKey(Collection, related_name='items', on_delete=models.CASCADE)
    blue = models.SmallIntegerField(null=True, blank=True)
    green = models.SmallIntegerField(null=True, blank=True)
    red = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ItemManager()

    class Meta:
        db_table = "items"

    def __str__(self):
        return self.name

@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Item)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Item.objects.get(pk=instance.pk).image
    except Item.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Match(object):
    def __init__(self, **kwargs):
        for field in ('image', 'collection', 'delta'):
            setattr(self, field, kwargs.get(field, None))
