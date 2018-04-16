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


class Experiment(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=u'Название')
    description = models.TextField(blank=True, verbose_name=u'Описание')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

    class Meta:
        verbose_name = u'Эксперимент'
        verbose_name_plural = u'Эксперименты'

    def __unicode__(self):
        return unicode(self.name)


class Movie(TimeStampedModel):
    src = models.FileField(upload_to='uploads/tank/movies', verbose_name=u'Запись', help_text=u'Видео, гифка')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='movies')

    class Meta:
        verbose_name = u'Видео'
        verbose_name_plural = u'Видео'

    def __unicode__(self):
        return unicode(self.src)


class Images(TimeStampedModel):
    """ Store restaurant images """
    src = models.ImageField(upload_to='uploads/tank/images', max_length=255, verbose_name=u'Фото')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='images')

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

    def __unicode__(self):
        return unicode(self.src)


class Data(TimeStampedModel):
    src = models.FileField(upload_to='uploads/tank/data', verbose_name=u'Данные')
    experiment = models.ForeignKey(Experiment, verbose_name=u'Эксперимент', related_name='data')

    class Meta:
        verbose_name = u'Данные'
        verbose_name_plural = u'Данные'

    def __unicode__(self):
        return unicode(self.src)
