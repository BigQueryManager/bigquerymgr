# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 22:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('query_text', models.CharField(max_length=255)),
                ('schedule', models.CharField(max_length=255)),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('run_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QueryInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_url', models.URLField(max_length=255)),
                ('visual_url', models.URLField(max_length=255)),
                ('status', models.CharField(default='Pending', max_length=16)),
                ('queries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='queries.Queries')),
            ],
        ),
    ]
