# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from .serializers import CollectionSerializer, ItemSerializer, MatchSerializer
from .models import Collection, Item
from utils.image import pixelate, get_average_color

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    # def create(self, request):
    #     # image = request.FILES.get('image', None)
    #     # pixelate('test')
    #     # ItemSerializer(request.data)
    #     # print get_average_color(image)
    #     serializer = ItemSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer

    def create(self, request):
        print request.FILES
        pixelate('test')
        return Response(True)
