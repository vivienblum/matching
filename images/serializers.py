from rest_framework.serializers import ModelSerializer
from django.conf import settings
from utils.image import get_average_color
from .models import Collection, Item

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name')

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'image', 'collection')

    def create(self, validated_data):
        item = Item(**validated_data)

        # TODO calculate color
        # item.name = validated_data['image']
        # request
        item.save()
        get_average_color(item.image)
        return item
