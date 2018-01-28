# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-28 23:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('ready', 'Ready'), ('published', 'Published')], default='draft', max_length=10)),
                ('title', models.CharField(max_length=250)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from='title', unique=True)),
                ('content', models.TextField()),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['-date_published', '-created'],
            },
        ),
        migrations.CreateModel(
            name='BlogAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.TextField()),
                ('position', models.CharField(blank=True, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')], max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
