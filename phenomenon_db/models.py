from django.db import models
from django_extensions.db.models import TimeStampedModel
from geoposition.fields import GeopositionField


class SeaPhenomenon(TimeStampedModel):
    TSUNAMI = 0
    METEO_TSUNAMI = 1
    CYCLONE = 2
    SURGE = 3
    STORM_SURGE = 4
    FREAK_WAVE = 5
    UPWELLING = 6

    TYPES = (
        (TSUNAMI, 'Цунами'),
        (METEO_TSUNAMI, 'Метео-цунами'),
        (CYCLONE, 'Циклон'),
        (SURGE, 'Нагон'),
        (STORM_SURGE, 'Штормовой нагон'),
        (FREAK_WAVE, 'Аномальное большая волна'),
        (UPWELLING, 'Сгон'),
    )

    type_phenomenon = models.PositiveIntegerField(default=TSUNAMI, choices=TYPES, verbose_name='Тип явления')
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name='Название события',
                            help_text='Если есть')
    place = models.CharField(verbose_name='Место', max_length=255, help_text='Например: Южный Сахалин')
    position = GeopositionField(blank=True, verbose_name='Координаты', help_text='Если есть')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')
    date_start = models.DateField(blank=True, null=True, verbose_name='Дата от')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата до')
    wind_speed = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ветер')
    height_wave = models.CharField(blank=True, null=True, max_length=255, verbose_name='Высота волн')
    source_link = models.URLField(blank=True, null=True, max_length=500, verbose_name='Источник', help_text='Ссылка')
    comments = models.TextField(blank=True, null=True, verbose_name='Комментарии')

    def __str__(self):
        return self.get_type_phenomenon_display()

    class Meta:
        verbose_name = 'Морское явление'
        verbose_name_plural = 'Морские явления'
