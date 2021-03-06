# Generated by Django 2.1.5 on 2019-04-13 18:48

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_collection_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='match_image')),
                ('finished', models.BooleanField(default=True)),
                ('rows_progress', models.FloatField(default=0)),
                ('pattern', jsonfield.fields.JSONField(null=True)),
                ('items', jsonfield.fields.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collection_match', to='images.Collection')),
            ],
        ),
    ]
