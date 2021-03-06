# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-26 00:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430')),
                ('cv_file', models.FileField(blank=True, null=True, upload_to='users/cv/', verbose_name='\u0424\u0430\u0439\u043b CV')),
                ('is_subscribe', models.BooleanField(default=True, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u043d\u0430 email \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('authors', models.CharField(max_length=200, verbose_name='\u0410\u0432\u0442\u043e\u0440\u044b')),
                ('abstract', models.TextField(blank=True, max_length=2000, null=True, verbose_name='\u0410\u043d\u043d\u043e\u0442\u0430\u0446\u0438\u044f')),
                ('file', models.FileField(blank=True, null=True, upload_to='articles/', verbose_name='\u0424\u0430\u0439\u043b \u0441 \u0442\u0435\u043a\u0442\u043e\u043c \u0441\u0442\u0430\u0442\u044c\u0438')),
                ('link', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('source', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0416\u0443\u0440\u043d\u0430\u043b, \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f')),
                ('year', models.IntegerField(verbose_name='\u0413\u043e\u0434')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u0442\u044c\u044f',
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u044c\u0438',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f')),
            ],
            options={
                'verbose_name': '\u0421\u043e\u0431\u044b\u0442\u0438\u0435',
                'verbose_name_plural': '\u0421\u043e\u0431\u044b\u0442\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u043d\u0430 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u043e\u043c')),
                ('title', models.CharField(max_length=200, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b',
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200, verbose_name='\u0424\u0418\u041e')),
                ('degree', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c')),
                ('rank', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0423\u0447\u0451\u043d\u043e\u0435 \u0437\u0432\u0430\u043d\u0438\u0435')),
                ('position', models.CharField(max_length=50, verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c')),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lmnad.Account')),
            ],
            options={
                'verbose_name': '\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a',
                'verbose_name_plural': '\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Protection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='\u0410\u0432\u0442\u043e\u0440')),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442\u044b')),
                ('message', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0449\u0438\u0442\u0430',
                'verbose_name_plural': '\u0417\u0430\u0449\u0438\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f')),
            ],
            options={
                'verbose_name': '\u0421\u0435\u043c\u0438\u043d\u0430\u0440',
                'verbose_name_plural': '\u0421\u0435\u043c\u0438\u043d\u0430\u0440\u044b',
            },
        ),
    ]
