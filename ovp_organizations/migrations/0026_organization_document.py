# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-12 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0025_auto_20180112_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='document',
            field=models.CharField(blank=True, default=None, max_length=40, null=True, verbose_name='document'),
        ),
    ]