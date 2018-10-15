# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from constance import config
from django.core.mail import send_mail
from django.template.loader import get_template
from django_extensions.db.models import TimeStampedModel
from filebrowser.fields import FileBrowseField


class Images(TimeStampedModel):
    """ Store restaurant images """
    file = models.ImageField(upload_to='uploads/images', max_length=255, verbose_name=u'Изображение')

    class Meta:
        verbose_name = u'Изображение'
        verbose_name_plural = u'Изображение'

    def __unicode__(self):
        return unicode(self.file)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name=u'Персональная страница',
                            help_text=u'В произвольной форме')
    photo = models.ForeignKey(Images, null=True, blank=True, verbose_name=u'Фото')
    cv_file = models.FileField(upload_to='uploads/users/cv/', null=True, blank=True, verbose_name=u'Файл CV',
                               help_text=u'Прикрепить существующее CV')
    is_subscribe = models.BooleanField(default=True, verbose_name=u'Подписка на email оповещения')

    def __unicode__(self):
        if self.user.get_full_name():
            return unicode(self.user.get_full_name())
        else:
            return unicode(self.user)

    def get_absolute_url(self):
        return "/profile/{}/".format(self.user.username)

    def get_profile_export_url(self):
        return "/user/{}/export/publication/".format(self.user.username)

    def get_profile_add_pub_url(self):
        return "/user/{}/add/publication/".format(self.user.username)

    def get_profile_edit_pub_url(self):
        return "/user/{}/edit/publication/".format(self.user.username)

    def get_profile_cancel_url(self):
        return "/user/{}/cancel/".format(self.user.username)

    def get_profile_add_journal_url(self):
        return "/user/{}/add/journal/".format(self.user.username)

    def get_profile_add_author_url(self):
        return "/user/{}/add/author/".format(self.user.username)

    def is_worker(self):
        try:
            if self.people.status:
                # work status
                return True
        except People.DoesNotExist:
            pass
        return False

    def is_author(self):
        if self.author.first():
            return True
        else:
            return False

    def get_full_name(self):
        if self.author.first():
            return self.author.first().get_full_name()

        try:
            return self.people.fullname
        except People.DoesNotExist:
            return self

    class Meta:
        verbose_name = 'Персональная страница'
        verbose_name_plural = 'Персональные страницы'


class People(models.Model):
    fullname = models.CharField(max_length=200, verbose_name=u'ФИО')
    degree = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Степень')
    rank = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Учёное звание')
    position = models.CharField(max_length=50, verbose_name=u'Должность')
    account = models.OneToOneField(Account, blank=True, null=True, verbose_name=u'Аккаунт сотрудника',
                                   related_name='people', help_text=u'Если есть')
    science_index = models.TextField(max_length=500, null=True, blank=True, verbose_name=u'Научный индекс')
    status = models.BooleanField(default=True, verbose_name=u'Работает')
    date_start = models.DateField(blank=True, null=True, verbose_name=u'Дата начала работы')
    date_end = models.DateField(blank=True, null=True, verbose_name=u'Дата конца работы')
    order_by = models.PositiveIntegerField(verbose_name=u'Сортировать', default=0)

    class MPTTMeta:
        order_insertion_by = ['order_by']

    def get_absolute_url(self):
        if self.account:
            return "/profile/%s/" % self.account.user.username

    def __unicode__(self):
        return unicode(self.fullname)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Protection(models.Model):
    author = models.CharField(max_length=100, verbose_name=u'Автор')
    title = models.CharField(max_length=200, verbose_name=u'Название работы')
    message = models.TextField(verbose_name=u'Текст')
    date = models.DateField(blank=True, verbose_name=u'Дата')
    is_send_email = models.BooleanField(default=False, verbose_name=u'Сделать рассылку')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            template_text = get_template('lmnad/send_protection_email.txt')
            context = {
                'title': self.title,
                'author': self.author,
                'text': self.message,
                'date': self.date
            }

            recipient_list = config.LIST_EMAILS.split(',')
            body_text = template_text.render(context)
            send_mail(
                self.title,
                body_text,
                from_email='lmnad@nntu.ru',
                recipient_list=recipient_list,
                fail_silently=True
            )

        super(Protection, self).save(*args, **kwargs)

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


class Grant(models.Model):
    type = models.CharField(max_length=50, verbose_name=u'Тип')
    number = models.CharField(max_length=50, verbose_name=u'Номер')
    name = models.CharField(max_length=500, verbose_name=u'Текст')
    head = models.ManyToManyField(People, related_name='head', verbose_name=u'Руководители')
    members = models.ManyToManyField(People, related_name='members', verbose_name=u'Участники')
    date_start = models.DateField(verbose_name=u'Дата начала')
    date_end = models.DateField(verbose_name=u'Дата конца')
    abstract = models.TextField(blank=True, verbose_name=u'Аннотация')
    reference = models.CharField(max_length=500, blank=True, verbose_name=u'Ссылка на грант')
    reference_result = models.CharField(max_length=500, blank=True, verbose_name=u'Cсылка на результаты конкурса')

    def get_absolute_url(self):
        return "/grants/%s/" % self.number

    def get_name_head(self):
        try:
            person = People.objects.get(account=self.head)
        except:
            return self.head.user.get_short_name()
        else:
            return person.fullname

    def export(self):
        date_start = self.date_start.strftime('%d.%m.%Y') if self.date_start else ''
        date_end = self.date_end.strftime('%d.%m.%Y') if self.date_end else ''
        result = '{type} {number}; {name}, {date_start} - {date_end}'.format(type=self.type,
                                                                             number=self.number,
                                                                             name=self.name,
                                                                             date_start=date_start,
                                                                             date_end=date_end)
        return result

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = 'Грант'
        verbose_name_plural = 'Гранты'


class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название проекта на английском',
                            help_text=u'Используется для перехода на страницу')
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    short_text = models.TextField(blank=True, null=True, verbose_name=u'Короткое описание')
    text = models.TextField(verbose_name=u'Текст')
    link = models.CharField(max_length=100, blank=True, verbose_name=u'Ссылка на проект')
    is_only_user = models.BooleanField(default=False, verbose_name=u'Доступно зарегистрированным пользователям')
    order_by = models.PositiveIntegerField(verbose_name=u'Сортировать', default=0)

    class MPTTMeta:
        order_insertion_by = ['order_by']

    def get_absolute_url(self):
        return "%s/" % self.name

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Краткое описание')
    full_text = models.TextField(blank=True, verbose_name=u'Полный текст, отчёт')
    date = models.DateTimeField(verbose_name=u'Дата и время')
    is_send_email = models.BooleanField(default=False, verbose_name=u'Сделать рассылку')
    images = models.ManyToManyField(Images, blank=True, verbose_name=u'Изображения')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            send_email(self.title, self.text, self.date)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "%s/" % self.pk

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Краткое описание')
    full_text = models.TextField(blank=True, verbose_name=u'Полный текст, отчёт')
    date = models.DateTimeField(verbose_name=u'Дата и время')
    is_send_email = models.BooleanField(default=False, verbose_name=u'Сделать рассылку')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            send_email(self.title, self.text, self.date)
        super(Seminar, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "%s/" % self.pk

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Семинар'
        verbose_name_plural = 'Семинары'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Название')
    authors = models.CharField(max_length=200, verbose_name=u'Авторы')
    abstract = models.TextField(max_length=2000, null=True, blank=True, verbose_name=u'Аннотация')
    file = models.FileField(upload_to='uploads/articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Ссылка')
    source = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Журнал, страницы')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    year = models.IntegerField(verbose_name=u'Год')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = '(Old) Статья'
        verbose_name_plural = '(Old) Статьи'


class Wiki(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(max_length=5000, verbose_name=u'Текст')
    link = models.CharField(max_length=255, blank=True, verbose_name=u'Ссылка')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = u'Wiki'
        verbose_name_plural = u'Wiki'


def send_email(title, text, date):
    template_text = get_template('lmnad/send_email.txt')
    context = {
        'title': title,
        'text': text,
        'date': date
    }

    recipient_list = config.LIST_EMAILS.split(',')
    body_text = template_text.render(context)
    send_mail(
        title,
        body_text,
        from_email='lmnad@nntu.ru',
        recipient_list=recipient_list,
        fail_silently=True,
        html_message=body_text
    )
