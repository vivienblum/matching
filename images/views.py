# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from .serializers import CollectionSerializer, ItemSerializer, MatchSerializer
from .models import Collection, Item, Match
from utils.image import pixelate, get_average_color
from django_filters.rest_framework import DjangoFilterBackend

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'available', 'has_popularity')

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('name')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get("name", instance.name)
        instance.popularity = request.data.get("popularity", instance.popularity)
        instance.save()

        return Response(instance.as_json())

class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    # def create(self, request):
    #     image = request.FILES.get('image', None)
    #     collection = request.data.get('collection', None)
    #     delta = request.data.get('delta', None)
    #
    #     res = match(image, collection, delta)
    #
    #     if res:
    #         pattern, items = res
    #         serializer_item = ItemSerializer(items, many=True)
    #         return Response({'pattern': pattern, 'items': serializer_item.data}, status=200)
    #     else:
    #         return Response({'error': 'The image is too big!'}, status=429)
