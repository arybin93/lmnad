# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

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


class Experiment(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=u'Название')
    description = models.TextField(blank=True, verbose_name=u'Описание')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

    class Meta:
        verbose_name = u'Эксперимент'
        verbose_name_plural = u'Эксперименты'

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return "/tank_exp/%s/" % self.id


class Movie(TimeStampedModel):
    file = models.FileField(upload_to='uploads/tank/movies', verbose_name=u'Запись', help_text=u'Видео, гифка')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='movies')

    class Meta:
        verbose_name = u'Видео'
        verbose_name_plural = u'Видео'

    def __unicode__(self):
        return unicode(self.file)


class Images(TimeStampedModel):
    """ Store restaurant images """
    file = models.ImageField(upload_to='uploads/tank/images', max_length=255, verbose_name=u'Фото')
    is_schema = models.BooleanField(default=False, verbose_name=u'Cхема эксперимента', help_text=u'Да, нет')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='images')

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

    def __unicode__(self):
        return unicode(self.file)

    def filename(self):
        return os.path.basename(self.file.name)


class Data(TimeStampedModel):
    file = models.FileField(upload_to='uploads/tank/data', verbose_name=u'Данные')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='data')

    class Meta:
        verbose_name = u'Данные'
        verbose_name_plural = u'Данные'

    def __unicode__(self):
        return unicode(self.file)

    @classmethod
    def name(self):
        print self.file.name.split('/')[-1]
        return self.file.name.split('/')[-1]
