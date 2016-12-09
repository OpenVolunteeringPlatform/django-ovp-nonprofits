# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 19:41
from __future__ import unicode_literals

from django.db import migrations

from ovp_organizations.models import Organization

def add_members(apps, schema_editor):
  for organization in Organization.objects.only('pk', 'members').all():
    organization.members.add(organization.owner)


def remove_members(apps, schema_editor):
  for organization in Organization.objects.only('pk', 'members').all():
    organization.members.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0007_organization_members'),
    ]

    operations = [
        migrations.RunPython(add_members, reverse_code=remove_members)
    ]
