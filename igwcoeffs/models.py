# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Calculation(TimeStampedModel):

    TYPE_POINT = 0
    TYPE_SECTION = 1
    TYPES = (
        (TYPE_POINT, u'Расчёт для одной точки'),
        (TYPE_SECTION, u'Расчёт для разреза')
    )

    BOTH_MODES = 0
    ONE_MODE = 1
    TWO_MODE = 2
    MODE_TYPES = (
        (BOTH_MODES, u'Двух мод'),
        (ONE_MODE, u'Первой моды'),
        (TWO_MODE, u'Второй моды')
    )

    name = models.CharField(max_length=255, verbose_name=u'Название расчёта')
    source_file = models.FileField(upload_to='uploads/igwcoeffs/sources', max_length=255,
                                   verbose_name=u'Файл с исходными данными')
    result_file = models.FileField(upload_to='uploads/igwcoeffs/results', max_length=255,
                                   verbose_name=u'Файл с результатом', blank=True, null=True)
    types = models.PositiveIntegerField(default=TYPE_POINT, choices=TYPES, verbose_name=u'Тип расчёта')
    mode = models.PositiveIntegerField(default=ONE_MODE, choices=MODE_TYPES, verbose_name=u'Расчёт для')
    email = models.CharField(max_length=55, blank=True, verbose_name=u'Email',
                             help_text=u'Для отправки результата расчёта на почту')

    class Meta:
        verbose_name = 'Расчёт'
        verbose_name_plural = 'Расчёты'

    def __unicode__(self):
        return unicode(self.name)
