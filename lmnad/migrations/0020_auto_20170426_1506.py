# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-26 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmnad', '0019_auto_20170426_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f'),
        ),
    ]
