# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-06 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmnad', '0006_project_short_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='order_by',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0421\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c'),
        ),
    ]
