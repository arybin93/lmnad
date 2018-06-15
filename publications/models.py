# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from lmnad.models import Account
from django_extensions.db.models import TimeStampedModel


class Journal(TimeStampedModel):
    """ Journal """
    name = models.CharField(unique=True, max_length=255, verbose_name=u'Название журнала, конференции')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Author(TimeStampedModel):
    """ Author """
    name = models.CharField(max_length=55, verbose_name=u'Имя')
    last_name = models.CharField(max_length=55, verbose_name=u'Фамилия')
    middle_name = models.CharField(max_length=55, blank=True, verbose_name=u'Отчество')
    user = models.ForeignKey(Account, blank=True, null=True,
                             verbose_name=u'Пользователь',
                             help_text=u'Если есть аккаунт')

    def __unicode__(self):
        full_name = '{} {}'.format(self.last_name, self.name)
        return unicode(full_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Publication(TimeStampedModel):
    """ Publication """
    ARTICLE = 'Article'
    TYPE = (
        (ARTICLE, u'Статья'),
    )

    type = models.CharField(max_length=55, default=ARTICLE, choices=TYPE, verbose_name=u'Тип публикации')
    title = models.CharField(max_length=200, verbose_name=u'Название')
    authors = models.ManyToManyField(Author, through='AuthorPublication', verbose_name=u'Авторы')
    journal = models.ForeignKey(Journal, blank=True, verbose_name=u'Журнал, конференция')
    year = models.IntegerField(verbose_name=u'Год')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    volume = models.CharField(max_length=55, blank=True, verbose_name='Том, номер')
    pages = models.CharField(max_length=55, blank=True, verbose_name='Страницы')
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'Номер свидетельства')
    link = models.CharField(max_length=200, blank=True, verbose_name=u'Ссылка', help_text=u'Если есть')
    doi = models.CharField(max_length=200, blank=True, verbose_name=u'DOI', help_text=u'Если есть')
    is_rinc = models.BooleanField(default=False, verbose_name=u'Входит в РИНЦ',
                                  help_text=u'Отметьте галочку, если публикация входит в РИНЦ')
    is_wos = models.BooleanField(default=False, verbose_name=u'Входит в WOS',
                                    help_text=u'Отметьте галочку, если публикация входит в Web of Science')
    is_scopus = models.BooleanField(default=False, verbose_name=u'Входит в Scopus',
                                    help_text=u'Отметьте галочку, если публикация входит в Scopus')
    file = models.FileField(upload_to='uploads/articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    is_can_download = models.BooleanField(default=False, verbose_name=u'Можно скачать',
                                          help_text=u'Отметьте галочку, если файл доступен для скачивания')
    is_show = models.BooleanField(default=True, verbose_name=u'Показывать на сайте',
                     help_text = u'Отметьте галочку, чтобы публикация была доступна на сайте')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class AuthorPublication(models.Model):
    """ Author Publication connection """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=u'Автор')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name=u'Публикация')
    order_by = models.PositiveIntegerField(default=0, verbose_name=u'Порядок отображения', help_text=u'От 0 - 100')

    def __unicode__(self):
        return unicode(self.author.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
