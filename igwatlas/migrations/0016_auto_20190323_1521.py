# Generated by Django 2.0.10 on 2019-03-23 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lmnad', '0034_auto_20181019_1354'),
        ('igwatlas', '0015_record_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='is_verified',
            field=models.BooleanField(default=True, help_text='Поставьте галочку, если источник проверен', verbose_name='Проверено'),
        ),
        migrations.AddField(
            model_name='source',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source', to='lmnad.Account', verbose_name='Пользователь'),
        ),
    ]