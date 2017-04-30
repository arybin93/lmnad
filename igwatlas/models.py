# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from geoposition.fields import GeopositionField

# IGWAtlas
class Source(models.Model):
    source_short = models.CharField(max_length=255, verbose_name=u'Краткое описание')
    source = models.TextField(verbose_name=u'Описание')
    file = models.FileField(upload_to='uploads/igwatlas/sources', null=True, blank=True,
                            verbose_name="Файл для источника", help_text=u'Если есть')
    link = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name=u'Ссылка', help_text=u'Если есть')

    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'

    def __unicode__(self):
        return unicode(self.source_short)

class Record(models.Model):
    MAP = 0
    GRAPHIC = 1
    SATELLITE = 2
    RECORD = 3
    TABLE = 4

    TYPES = (
        (MAP, u'Карта'),
        (GRAPHIC, u'График'),
        (SATELLITE, u'Спутниковый снимок'),
        (RECORD, u'Запись'),
        (TABLE, u'Таблица')
    )

    position = GeopositionField(verbose_name=u'Координаты')
    types = models.TextField(verbose_name=u'Тип', help_text=u'Может быть несколько типов')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время наблюдения')
    date_start = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время начала наблюдений',
                                      help_text=u'Если есть')
    date_stop = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время конца наблюдений',
                                     help_text=u'Если есть')
    image = models.ImageField(upload_to='uploads/igwatlas/images', blank=True, verbose_name=u'Изображение')
    source = models.ManyToManyField(Source, verbose_name=u'Источник')
    page = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'Страница из источника')
    data = models.FileField(upload_to='uploads/igwatlas/data', null=True, blank=True,
                            verbose_name=u'Оцифрованные данные', help_text=u'Если есть')

    class Meta:
        verbose_name = u'Наблюдение'
        verbose_name_plural = u'Наблюдения'

    def __unicode__(self):
        return unicode(self.position)

