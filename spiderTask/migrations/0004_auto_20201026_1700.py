# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-10-26 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderTask', '0003_cveiteminfoadd_collections_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cveiteminfoadd',
            name='itemUrl',
            field=models.CharField(default='', max_length=500, verbose_name='itemUrl'),
        ),
    ]
