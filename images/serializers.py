from rest_framework.serializers import ModelSerializer, Serializer
from django.db import models
from django.db.models import Exists, OuterRef
from django.conf import settings
from utils.image import get_average_color, match
from .models import Collection, Item, Match
from celery import shared_task

@shared_task
def build_something():
  return 3

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'available')

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'image', 'collection', 'blue', 'green', 'red')

    def create(self, validated_data):
        item = Item(**validated_data)

        # res = q.enqueue(match, item.image, 1, 100)
        # res = q.enqueue('serializers.count_words_at_url', "item.image, 1, 100")
        # res = q.enqueue(count_words_a&t_url, "item.image, 1, 100")
        build_something.apply_async()

        color = get_average_color(item.image)
        itemDb = Item.objects.filter(blue=color[0], green=color[1], red=color[2], collection=item.collection)

        if itemDb:
            return itemDb[0]
        else:
            item.blue = color[0]
            item.green = color[1]
            item.red = color[2]
            item.save()

            return item

class MatchSerializer(Serializer):
    image = models.ImageField()
    collection = models.IntegerField()
    delta = models.SmallIntegerField(null=True, blank=True)

    def create(self, validated_data):
        return Match(**validated_data)
