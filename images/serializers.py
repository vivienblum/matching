from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
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
        fields = ('id', 'name', 'image', 'collection', 'color')

    def create(self, validated_data):
        item = Item(**validated_data)

        item.save()
        item.color = get_average_color(item.image)
        item.save()

        return item

class MatchSerializer(Serializer):
    amount = IntegerField(read_only=True)

    def create(self, validated_data):
        return Match(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
