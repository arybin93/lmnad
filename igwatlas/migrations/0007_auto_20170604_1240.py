# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-06-04 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igwatlas', '0006_auto_20170604_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='uploads/igwatlas/sources', verbose_name='\u0424\u0430\u0439\u043b'),
        ),
    ]
