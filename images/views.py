# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import CollectionSerializer, ItemSerializer
from .models import Collection, Item

class CollectionViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class ItemViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
