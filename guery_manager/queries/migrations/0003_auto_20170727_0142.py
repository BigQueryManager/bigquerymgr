# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 01:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0002_queries_dataset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queries',
            old_name='dataset',
            new_name='project',
        ),
    ]