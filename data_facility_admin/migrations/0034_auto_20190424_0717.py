# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-24 11:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_facility_admin', '0033_auto_20190312_1416'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
    ]