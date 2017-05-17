# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from geoposition.fields import GeopositionField

class File(models.Model):
    path = models.FilePathField(path='uploads/igwatlas/sources', blank=True, null=True, verbose_name=u'Путь к файлу')
    file = models.FileField(upload_to='uploads/igwatlas/sources', blank=True, null=True, verbose_name=u'Файл')

    class Meta:
        verbose_name = u'Файл'
        verbose_name_plural = u'Файлы'

    def __unicode__(self):
        if self.path:
            return unicode(self.path)
        else:
            return unicode(self.file)

# IGWAtlas
class Source(models.Model):
    source_short = models.CharField(max_length=255, verbose_name=u'Краткое описание')
    source = models.TextField(verbose_name=u'Описание')
    files = models.ManyToManyField(File, blank=True, verbose_name=u'Файлы для источника',
                                  help_text=u'Один источник может быть представлен в нескольких файлах')
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
    types = models.TextField(verbose_name=u'Тип', help_text=u'Поддерживается несколько типов')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время наблюдения')
    date_start = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время начала наблюдений',
                                      help_text=u'Если есть')
    date_stop = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время конца наблюдений',
                                     help_text=u'Если есть')
    image = models.ImageField(upload_to='uploads/igwatlas/images', blank=True, verbose_name=u'Изображение')
    source = models.ManyToManyField(Source, verbose_name=u'Источник')
    page = models.CharField(max_length=15, blank=True, null=True, verbose_name=u'Страницы из источника')
    data = models.FileField(upload_to='uploads/igwatlas/data', null=True, blank=True,
                            verbose_name=u'Оцифрованные данные', help_text=u'Если есть')
    text = models.TextField(blank=True, null=True, verbose_name=u'Описание для наблюдения')
    file = models.ForeignKey(File, blank=True, null=True, verbose_name=u'Файл, источник изображения',
                             help_text=u'Если источник представлен одним файлом, данное поле можно не заполнять')

    class Meta:
        verbose_name = u'Наблюдение'
        verbose_name_plural = u'Наблюдения'

    def __unicode__(self):
        return unicode(self.position)

    def get_text_types(self):
        text = ''
        types = self.types.strip('[').strip(']')
        types_list = types.split(',')
        type_dict = self.get_types()

        for type in types_list:
            index = int(type)
            text = text + type_dict[index] + '; '

        return text

    @staticmethod
    def get_types():
        types = {}
        for i in Record.TYPES:
            types.update({
                i[0]: i[1]
            })
        return types