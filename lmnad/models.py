# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page = models.TextField(null=True, blank=True, verbose_name=u'Персональная страница')
    photo = models.ImageField(null=True, blank=True, verbose_name=u'Фото')
    fullname = models.CharField(max_length=100, verbose_name=u'ФИО')
    degree = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'Степень')
    position = models.CharField(max_length=50, verbose_name=u'Должность')

class Protection(models.Model):
    author = models.CharField(max_length=100, verbose_name=u'Автор')
    title = models.CharField(max_length=200, verbose_name=u'Название работы')
    message = models.TextField(verbose_name=u'Текст')
    date = models.DateField(verbose_name=u'Дата')

class Page(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название')
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')

    '''
    def save(self):
        print 'send email'
        if self.id:
            print 'send email'
            send_mail(
                'Subject here',
                'Here is the message.',
                'arybin93@gmail.com',
                ['artem.rybin93@yandex.ru'],
                fail_silently=False,
            )

            datatuple = (
                ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
                ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
            )
            send_mass_mail(datatuple)

        return super(Seminar, self).save()
     '''

class People(models.Model):
    fullname = models.CharField(max_length=200, verbose_name=u'ФИО')
    degree = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Степень')
    position = models.CharField(max_length=50, verbose_name=u'Должность')


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Название')
    authors = models.CharField(max_length=200, verbose_name=u'Авторы')
    abstract = models.CharField(max_length=2000,null=True, blank=True, verbose_name=u'Аннотация')
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Ссылка')
    source = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Журнал, страницы')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    year = models.IntegerField(verbose_name=u'Год')


