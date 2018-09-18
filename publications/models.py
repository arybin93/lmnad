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
    user = models.ForeignKey(Account, blank=True, null=True, related_name='author',
                             verbose_name=u'Пользователь',
                             help_text=u'Если есть аккаунт')

    def __unicode__(self):
        full_name = '{} {}'.format(self.last_name, self.name)
        return unicode(full_name)

    def get_full_name(self):
        if self.middle_name:
            full_name = '{} {} {}'.format(self.last_name, self.name, self.middle_name)
        else:
            full_name = '{} {}'.format(self.last_name, self.name)
        return unicode(full_name)

    def get_short_name(self):
        short_name = self.name[0]
        if self.middle_name:
            short_middle = self.middle_name[0]
            author_str = u"{} {}. {}.".format(self.last_name,
                                              short_name,
                                              short_middle)
        else:
            author_str = u"{} {}.".format(self.last_name,
                                          short_name)
        return author_str

    def get_short_name_harvard(self):
        short_name = self.name[0]
        if self.middle_name:
            short_middle = self.middle_name[0]
            author_str = u"{}, {}. {}.,".format(self.last_name,
                                                short_name,
                                                short_middle)
        else:
            author_str = u"{}, {}.,".format(self.last_name,
                                            short_name)
        return author_str

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Publication(TimeStampedModel):
    """ Publication """
    ARTICLE = 'Article'
    MONOGRAPH = 'Monograph'
    GROUP_MONOGRAPH = 'Group Monograph'
    PROCEEDINGS = 'Proceedings'
    THESES_CONFERENCE = 'Theses conference'
    TEACHING_MATERIALS = 'Teaching materials'
    PATENT = 'Patent'

    TYPE = (
        (ARTICLE, u'Статья в периодическом издании'),
        (MONOGRAPH, u'Авторская монография'),
        (GROUP_MONOGRAPH, u'Глава в коллективной монографии'),
        (PROCEEDINGS, u'Статья в сборнике трудов конференции'),
        (THESES_CONFERENCE, u'Тезисы конференции'),
        (TEACHING_MATERIALS, u'Учебно-методические материалы'),
        (PATENT, u'Свидетельство о регистрации права на программный продукт'),
    )

    type = models.CharField(max_length=55, default=ARTICLE, choices=TYPE, verbose_name=u'Тип публикации')
    title = models.CharField(max_length=200, db_index=True, verbose_name=u'Название')
    authors = models.ManyToManyField(Author, through='AuthorPublication', verbose_name=u'Авторы')
    journal = models.ForeignKey(Journal, blank=True, verbose_name=u'Журнал, конференция')
    year = models.IntegerField(verbose_name=u'Год')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    volume = models.CharField(max_length=55, blank=True, verbose_name='Том')
    issue = models.CharField(max_length=55, blank=True, verbose_name=u'Номер журнала')
    pages = models.CharField(max_length=55, blank=True, verbose_name='Страницы')
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'Номер свидетельства')
    link = models.CharField(max_length=200, blank=True, verbose_name=u'Ссылка', help_text=u'Если есть')
    doi = models.CharField(max_length=200, blank=True, verbose_name=u'DOI', help_text=u'Если есть')
    is_rinc = models.BooleanField(default=False, verbose_name=u'Входит в РИНЦ',
                                  help_text=u'Отметьте галочку, если публикация входит в РИНЦ')
    is_vak = models.BooleanField(default=False, verbose_name=u'Входит в ВАК',
                                 help_text=u'Отметьте галочку, если публикация входит в ВАК')
    is_wos = models.BooleanField(default=False, verbose_name=u'Входит в WOS',
                                    help_text=u'Отметьте галочку, если публикация входит в Web of Science')
    is_scopus = models.BooleanField(default=False, verbose_name=u'Входит в Scopus',
                                    help_text=u'Отметьте галочку, если публикация входит в Scopus')
    is_other_db = models.BooleanField(default=False, verbose_name=u'Входит в другие базы данных')
    file = models.FileField(upload_to='uploads/articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    is_can_download = models.BooleanField(default=False, verbose_name=u'Можно скачать',
                                          help_text=u'Отметьте галочку, если файл доступен для скачивания')
    is_show = models.BooleanField(default=True, verbose_name=u'Показывать на сайте',
                     help_text = u'Отметьте галочку, чтобы публикация была доступна на сайте')

    def __unicode__(self):
        return unicode(self.title)

    def source(self):
        """ Get journal, issue, volume, pages """
        result = '{journal} {volume}{issue} {pages}'

        journal = '{},'.format(self.journal.name) if self.journal else ''
        volume = ''
        issue = ''
        pages = ''
        if self.volume and self.issue:
            volume = self.volume
            issue = '({}),'.format(self.issue)

        if self.pages:
            pages = 'pp. {pages},'.format(pages=self.pages)

        return result.format(
                             journal=journal,
                             volume=volume,
                             issue=issue,
                             pages=pages)

    def get_harvard(self):
        """ Get reference in Harvard format, examples:
        Alpers, W., Pahl, U. & Gross, G., 1998.
        Katabatic wind fields in coastal areas studied by ERS-1 synthetic aperture radar imagery and numerical modeling.
        Journal of Geophysical Research: Oceans, 103(C4), pp.7875–7886.
        Available at: http://dx.doi.org/10.1029/97jc01774. Volume 103, Issue C4
        ---
        Ocampo-Torres, F.J., 2000.
        Spatial Variations of Ocean Wave Spectra in Coastal Regions from RADARSAT and ERS Synthetic Aperture Radar Images.
        Available at: http://dx.doi.org/10.4095/219636.
        """
        result = '{authors} {year}. {title}. {journal} {volume}{issue} {pages} {doi}'

        result_authors = ''
        if self.authors:
            authors = self.authors.order_by('authors__order_by')
            if authors.count() > 1:
                len_authors = authors.count() - 1
                authors_list = []
                author_str = ''
                for index, author in enumerate(authors):
                    author_str = '{}'.format(author.get_short_name_harvard())
                    if index == len_authors:
                        author_str = '& {}'.format(author.get_short_name_harvard())
                    else:
                        authors_list.append(author_str)

                result_authors = ' '.join(authors_list) + author_str
            else:
                result_authors = '{}'.format(authors.first().get_short_name_harvard())

        year = str(self.year) if self.year else ''
        title = self.title if self.title else ''
        journal = '{},'.format(self.journal.name) if self.journal else ''
        doi = 'doi: {}'.format(self.doi) if self.doi else ''

        volume = ''
        issue = ''
        pages = ''
        if self.volume and self.issue:
            volume = self.volume
            issue = '({}),'.format(self.issue)

        if self.pages:
            pages = 'pp. {pages},'.format(pages=self.pages)

        return result.format(authors=result_authors,
                             year=year,
                             title=title,
                             journal=journal,
                             volume=volume,
                             issue=issue,
                             pages=pages,
                             doi=doi)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class AuthorPublication(models.Model):
    """ Author Publication connection """
    author = models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE, verbose_name=u'Автор')
    publication = models.ForeignKey(Publication, related_name='publications', on_delete=models.CASCADE, verbose_name=u'Публикация')
    order_by = models.PositiveIntegerField(default=0, verbose_name=u'Порядок отображения', help_text=u'От 0 - 100')

    def __unicode__(self):
        return unicode(self.author.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
