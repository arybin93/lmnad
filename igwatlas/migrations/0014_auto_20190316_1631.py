# Generated by Django 2.0.10 on 2019-03-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igwatlas', '0013_record_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
