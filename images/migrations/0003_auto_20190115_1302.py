# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-15 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_item_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='color',
        ),
        migrations.AddField(
            model_name='item',
            name='blue',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='green',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='red',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
