# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from .serializers import CollectionSerializer, ItemSerializer, MatchSerializer
from .models import Collection, Item
from utils.image import pixelate, get_average_color, match
# import json

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer

    def create(self, request):
        # print request.data
        # print MatchSerializer(request.data, many=True).data
        data = [{'image': request.FILES.get('image', None), 'collection': request.data.get('collection', None), 'delta': request.data.get('delta', None)}]
        serializer = MatchSerializer(data, many=True)
        res = MatchSerializer(data, many=True).data
        return Response(res)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            res = match(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if res:
            pattern, items = res
            serializer_item = ItemSerializer(items, many=True)
            return Response({'pattern': pattern, 'items': serializer_item.data}, status=200)
        else:
            return Response({'error': 'The image is too big!'}, status=429)
