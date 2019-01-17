# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
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
        delta = int(delta)
        blue_less = (
            self.filter(collection=collection)
                    .filter(blue__lte=color[0])
                    .filter(blue__gte=color[0] - delta)
                    .order_by('-blue')
        )
        blue_greather = (
            self.filter(collection=collection)
                    .filter(blue__gte=color[0])
                    .filter(blue__lte=color[0] + delta)
                    .order_by('blue')
        )
        matches_blue = list(chain(blue_less, blue_greather))

        green_less = (
            self.filter(collection=collection)
                    .filter(green__lte=color[1])
                    .filter(green__gte=color[1] - delta)
                    .order_by('-green')
        )
        green_greather = (
            self.filter(collection=collection)
                    .filter(green__gte=color[1])
                    .filter(green__lte=color[1] + delta)
                    .order_by('green')
        )
        matches_green = list(chain(green_less, green_greather))

        red_less = (
            self.filter(collection=collection)
                    .filter(red__lte=color[2])
                    .filter(red__gte=color[2] - delta)
                    .order_by('-red')
        )
        red_greather = (
            self.filter(collection=collection)
                    .filter(red__gte=color[2])
                    .filter(red__lte=color[2] + delta)
                    .order_by('red')
        )
        matches_red = list(chain(red_less, red_greather))
        items_match = list(set(matches_blue) & set(matches_green) & set(matches_red))
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


        # # print (list(set().intersection(matches_blue, matches_green, matches_red)))
        #
        # return (
        #     # self.filter(collection=collection)
        #     #         .filter(blue__lte=color[0] + delta)
        #     #         .filter(blue__gte=color[0] - delta)
        #     #         .filter(green__lte=color[1] + delta)
        #     #         .filter(green__gte=color[1] - delta)
        #     #         .filter(red__lte=color[2] + delta)
        #     #         .filter(red__gte=color[2] - delta)
        #     #         .first()
        #     #     )
        #     self.filter(collection=collection)
        #             .filter(blue__lte=color[0])
        #             .filter(blue__gte=color[0] - delta)
        #             .filter(green__lte=color[1] + delta)
        #             .filter(green__gte=color[1] - delta)
        #             .filter(red__lte=color[2] + delta)
        #             .filter(red__gte=color[2] - delta)
        #             .first()
        #         )

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
