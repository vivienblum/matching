# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import CollectionSerializer, ItemSerializer, MatchSerializer
from .models import Collection, Item

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer

    def create(self, request):
        return JsonResponse(True, safe=False)
