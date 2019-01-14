# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Collection, Item

admin.site.register(Collection)
admin.site.register(Item)
