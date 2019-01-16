# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from .serializers import CollectionSerializer, ItemSerializer, MatchSerializer
from .models import Collection, Item
from utils.image import pixelate, get_average_color, match

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer

    def create(self, request):
        res = match(request.FILES.get('image', None))

        if res:
            pattern, items = res
            serializer_item = ItemSerializer(items, many=True)
            return Response({'pattern': [], 'items': serializer_item.data}, status=200)
        else:
            return Response({'error': 'The image is too big!'}, status=429)
