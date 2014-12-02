# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import photolib.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', models.CharField(max_length=32, blank=True)),
                ('filename', models.CharField(help_text='A descriptive file name', max_length=128)),
                ('alt', models.CharField(help_text='alt attribute text for accessibility', max_length=255, blank=True)),
                ('caption', models.TextField(help_text='Recommended text to be used as photo caption.', blank=True)),
                ('notes', models.TextField(help_text='Any other notable information about this photo.', blank=True)),
                ('credits', models.TextField(help_text='Credits and copyright/left.', blank=True)),
                ('source', models.CharField(choices=[('Flickr', 'Flickr'), ('iStockphoto', 'iStockphoto')], max_length=32, blank=True)),
                ('source_url', models.URLField(help_text='Important when citation requires link to source.', blank=True)),
                ('image', models.ImageField(upload_to=photolib.models.upload_path)),
                ('uploaded', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('last_updated', models.DateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('photo_tags', taggit.managers.TaggableManager(verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', blank=True)),
            ],
            options={
                'ordering': ('-uploaded',),
            },
            bases=(models.Model,),
        ),
    ]
