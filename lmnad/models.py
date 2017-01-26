# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name=u'Персональная страница')
    cv_file = models.FileField(upload_to='users/cv/', null=True, blank=True, verbose_name=u'Файл CV')
    is_subscribe = models.BooleanField(default=True, verbose_name=u'Подписка на email оповещения')

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class People(models.Model):
    fullname = models.CharField(max_length=200, verbose_name=u'ФИО')
    degree = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Степень')
    rank = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Учёное звание')
    position = models.CharField(max_length=50, verbose_name=u'Должность')
    account = models.OneToOneField(Account, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.fullname)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Protection(models.Model):
    author = models.CharField(max_length=100, verbose_name=u'Автор')
    title = models.CharField(max_length=200, verbose_name=u'Название работы')
    message = models.TextField(verbose_name=u'Текст')
    date = models.DateField(verbose_name=u'Дата')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Защита'
        verbose_name_plural = 'Защиты'


class Page(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название страницы на английском')
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'



class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Семинар'
        verbose_name_plural = 'Семинары'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Название')
    authors = models.CharField(max_length=200, verbose_name=u'Авторы')
    abstract = models.TextField(max_length=2000, null=True, blank=True, verbose_name=u'Аннотация')
    file = models.FileField(upload_to='articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Ссылка')
    source = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Журнал, страницы')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    year = models.IntegerField(verbose_name=u'Год')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# IGWAtlas, need separate app for IGWAtlas
'''
class Record(models.Model):
    id = models.IntegerField(primary_key=True)
    longitude = models.TextField(db_column='Longitude')
    latitude = models.TextField(db_column='Latitude')
    date = models.DateField(db_column='Date', blank=True, null=True)
    types = models.TextField(db_column='Type')
    filenamefrom = models.TextField(db_column='FileNameFrom')
    pagefrom = models.TextField(db_column='PageFrom')
    picfilename = models.TextField(db_column='PicFileName')

    class Meta:
        db_table = 'records'


class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    source = models.TextField(db_column='Source')
    sourceshort = models.TextField(db_column='SourceShort')

    class Meta:
        db_table = 'sources'


class Relation(models.Model):
    id = models.IntegerField(primary_key=True)
    recid = models.ForeignKey(Record, db_column='RecID', on_delete=models.CASCADE)
    sourceid = models.ForeignKey(Source, db_column='SourceID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'relation'
'''

