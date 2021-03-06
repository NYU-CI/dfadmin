# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-13 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_facility_admin', '0008_auto_20181010_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='dataset_citation',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='ingested_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='temporal_coverage_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='temporal_coverage_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='dataset_citation',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='ingested_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='temporal_coverage_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='temporal_coverage_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
