from rest_framework.serializers import ModelSerializer, Serializer
from django.db import models
from django.conf import settings
from utils.image import get_average_color
from .models import Collection, Item, Match

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name')

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'image', 'collection', 'blue', 'green', 'red')

    def create(self, validated_data):
        item = Item(**validated_data)

        item.save()
        color = get_average_color(item.image)
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
