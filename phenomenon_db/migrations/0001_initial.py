# Generated by Django 2.0.12 on 2020-11-28 11:49

from django.db import migrations, models
import django_extensions.db.fields
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeaPhenomenon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('type_phenomenon', models.PositiveIntegerField(choices=[(0, 'Цунами'), (1, 'Метео-цунами'), (2, 'Циклон'), (3, 'Нагон'), (4, 'Штормовой нагон'), (5, 'Аномальное большая волна'), (6, 'Сгон')], default=0, verbose_name='Тип явления')),
                ('name', models.CharField(blank=True, help_text='Если есть', max_length=255, null=True, verbose_name='Название события')),
                ('place', models.CharField(help_text='Например: Южный Сахалин', max_length=255, verbose_name='Место')),
                ('position', geoposition.fields.GeopositionField(blank=True, help_text='Если есть', max_length=42, verbose_name='Координаты')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='Дата от')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Дата до')),
                ('wind_speed', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ветер')),
                ('height_wave', models.CharField(blank=True, max_length=255, null=True, verbose_name='Высота волн')),
                ('source_link', models.CharField(blank=True, help_text='Ссылка', max_length=500, null=True, verbose_name='Источник')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Комментарии')),
            ],
            options={
                'verbose_name_plural': 'Морские явления',
                'verbose_name': 'Морское явление',
            },
        ),
    ]
