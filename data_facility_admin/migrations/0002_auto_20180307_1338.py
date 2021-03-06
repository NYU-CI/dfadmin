# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 18:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_facility_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('public', models.BooleanField(default=False, help_text=b'Check this if everyone should have access to this schema. Please consider the related dataset permissions.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalDatabaseSchema',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('public', models.BooleanField(default=False, help_text=b'Check this if everyone should have access to this schema. Please consider the related dataset permissions.')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical database schema',
            },
        ),
        migrations.AlterField(
            model_name='historicaldataset',
            name='ldap_id',
            field=models.IntegerField(blank=True, db_index=True, editable=False, help_text=b'This is an internal LDAP information. Is it automatically generated.Don`t change this value unless you know what you`re doing.', null=True),
        ),
        migrations.AlterField(
            model_name='historicaldfrole',
            name='ldap_id',
            field=models.IntegerField(blank=True, db_index=True, editable=False, help_text=b'This is an internal LDAP information. Is it automatically generated.Don`t change this value unless you know what you`re doing.', null=True),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='ldap_id',
            field=models.IntegerField(blank=True, db_index=True, editable=False, help_text=b'This is an internal LDAP information. Is it automatically generated.Don`t change this value unless you know what you`re doing.', null=True),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='ldap_id',
            field=models.IntegerField(blank=True, db_index=True, editable=False, help_text=b'This is an internal LDAP information. Is it automatically generated.Don`t change this value unless you know what you`re doing.', null=True),
        ),
        migrations.AlterField(
            model_name='ldapobject',
            name='ldap_id',
            field=models.IntegerField(blank=True, editable=False, help_text=b'This is an internal LDAP information. Is it automatically generated.Don`t change this value unless you know what you`re doing.', null=True, unique=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='database_schema',
            field=models.ForeignKey(blank=True, help_text=b'The database schema that this dataset should be stored to.', null=True, on_delete=django.db.models.deletion.PROTECT, to='data_facility_admin.DatabaseSchema'),
        ),
        migrations.AddField(
            model_name='historicaldataset',
            name='database_schema',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_facility_admin.DatabaseSchema'),
        ),
    ]
