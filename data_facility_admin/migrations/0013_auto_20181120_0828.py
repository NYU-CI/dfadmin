# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_facility_admin', '0012_auto_20181115_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='source_archive',
            field=models.CharField(blank=True, help_text=b'Represents the source archive reference for this dataset in the that we got it from an archive instead of directly from the data owner/provider.', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='source_url',
            field=models.CharField(blank=True, help_text=b'Indicates the URL for the Source Archive, when this information is needed.', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='source_archive',
            field=models.CharField(blank=True, help_text=b'Represents the source archive reference for this dataset in the that we got it from an archive instead of directly from the data owner/provider.', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='source_url',
            field=models.CharField(blank=True, help_text=b'Indicates the URL for the Source Archive, when this information is needed.', max_length=256, null=True),
        ),
    ]
