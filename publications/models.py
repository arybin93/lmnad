# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.html import format_html

from lmnad.models import Account
from django_extensions.db.models import TimeStampedModel

from lmnad.utils import detect_language_text

RU = 'ru'
EN = 'en'

LANGUAGES = (
    (RU, u'Русский'),
    (EN, u'Английкий')
)


class Journal(TimeStampedModel):
    """ Journal """
    name = models.CharField(unique=True, max_length=255, verbose_name=u'Название журнала, конференции')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = 'Журнал/Конференция'
        verbose_name_plural = 'Журналы/Конференции'


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

    def get_short_name_harvard(self, lang=None):
        # set default value
        short_name = self.name[0]
        short_middle = self.middle_name[0] if self.middle_name else None
        last_name = self.last_name

        # set language
        if lang and lang == RU:
            short_name = self.name_ru[0]
            short_middle = self.middle_name_ru[0] if self.middle_name else None
            last_name = self.last_name_ru
        elif lang and lang == EN:
            if self.name_en and self.last_name_en:
                short_name = self.name_en[0]
                short_middle = self.middle_name_en[0] if self.middle_name else None
                last_name = self.last_name_en

        if short_middle:
            author_str = u"{}, {}. {}.,".format(last_name,
                                                short_name,
                                                short_middle)
        else:
            author_str = u"{}, {}.,".format(last_name,
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
    PATENT_BD = 'Patent_BD'

    TYPE = (
        (ARTICLE, u'Статья в периодическом издании'),
        (MONOGRAPH, u'Авторская монография'),
        (GROUP_MONOGRAPH, u'Глава в коллективной монографии'),
        (PROCEEDINGS, u'Статья в сборнике трудов конференции'),
        (THESES_CONFERENCE, u'Тезисы конференции'),
        (TEACHING_MATERIALS, u'Учебно-методические материалы'),
        (PATENT, u'Свидетельство о регистрации права на программный продукт'),
        (PATENT_BD, u'Свидетельство о регистрации права на базу данных')
    )

    type = models.CharField(max_length=55, default=ARTICLE, choices=TYPE, verbose_name=u'Тип публикации')
    title = models.CharField(max_length=200, db_index=True, verbose_name=u'Название')
    authors = models.ManyToManyField(Author, through='AuthorPublication', verbose_name=u'Авторы')
    journal = models.ForeignKey(Journal, blank=True, null=True, verbose_name=u'Журнал, конференция')
    year = models.IntegerField(verbose_name=u'Год')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата и время')
    volume = models.CharField(max_length=55, blank=True, verbose_name='Том')
    issue = models.CharField(max_length=55, blank=True, verbose_name=u'Номер журнала/конференции')
    pages = models.CharField(max_length=55, blank=True, verbose_name='Страницы')
    number = models.CharField(max_length=55, blank=True, null=True, verbose_name=u'Номер свидетельства')
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
    language = models.CharField(default=RU, max_length=10, choices=LANGUAGES, verbose_name=u'Основной язык публикации',
                                help_text=u'Используется для экпорта/цитирования на сайте в независимости'
                                          u' от выбранного языка на сайте')

    def save(self, *args, **kwargs):
        language = detect_language_text(self.title[:30])
        if language == RU:
            self.language = RU
        else:
            self.language = EN
        super(Publication, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    def information(self):
        """ Get information for publication, use in template """

        if self.type == self.PATENT or self.type == self.PATENT_BD:
            result = format_html(
                u'''
                <strong>Номер свидетельства №: </strong> {number} От: {date}
                ''',
                number=self.number,
                date=self.date.strftime('%d.%m.%Y') if self.date else u'-'
            )
        else:
            journal = '{},'.format(self.journal.name) if self.journal else ''
            issue = ''
            pages = ''
            if self.volume and self.issue:
                volume = self.volume
                issue = '({}),'.format(self.issue)
            else:
                volume = self.volume

            if self.pages:
                if RU == self.language:
                    pages = 'С. {pages},'.format(pages=self.pages)
                else:
                    pages = 'pp. {pages},'.format(pages=self.pages)

            doi = None
            if self.doi and ('http' not in self.doi or 'https' not in self.doi):
                doi = 'https://doi.org/' + self.doi

            result = format_html(
                u'''
                {journal} {volume}{issue} {pages} <strong>DOI: </strong> <a href="{doi_ref}">{doi}</a>
                ''',
                journal=journal,
                volume=volume,
                issue=issue,
                pages=pages,
                doi_ref=doi if doi else self.doi,
                doi=self.doi.replace('https://doi.org/', '') if self.doi else u'-',

            )

        return result

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
        year = str(self.year) if self.year else ''
        title = ''
        # set language for title
        if self.language == RU:
            title = self.title_ru if self.title_ru else self.title
        elif self.language == EN:
            title = self.title_en if self.title_en else self.title

        result_authors = ''
        if self.authors:
            authors = self.authors.order_by('authors__order_by')
            if authors.count() > 1:
                len_authors = authors.count() - 1
                authors_list = []
                author_str = ''
                for index, author in enumerate(authors):
                    author_str = '{}'.format(author.get_short_name_harvard(lang=self.language))
                    if index == len_authors:
                        author_str = '& {}'.format(author.get_short_name_harvard(lang=self.language))
                    else:
                        authors_list.append(author_str)

                result_authors = ' '.join(authors_list) + author_str
            else:
                result_authors = '{}'.format(authors.first().get_short_name_harvard(lang=self.language))

        if self.type == self.PATENT or self.type == self.PATENT_BD:
            result = u'{authors} {title}. {type_text} {number} от {date}'

            number = self.number if self.number else ''

            if self.type == self.PATENT:
                type_text = u'Свидетельство о государственной регистрации программы для ЭВМ №'
            else:
                type_text = u'Свидетельство о государственной регистрации базы данных №'

            date = self.date.strftime('%d.%m.%Y') if self.date else ''

            return result.format(authors=result_authors,
                                 title=title,
                                 type_text=type_text,
                                 number=number,
                                 date=date)
        else:
            result = '{authors} {year}. {title}. {journal} {volume}{issue} {pages} {doi}'
            doi = 'doi: {}'.format(self.doi) if self.doi else ''

            journal = '{},'.format(self.journal.name) if self.journal else ''
            # set language for title
            if self.language == RU:
                journal = self.journal.name_ru if self.journal.name_ru else self.journal.name
            elif self.language == EN:
                journal = self.journal.name_en if self.journal.name_en else self.journal.name

            volume = ''
            issue = ''
            pages = ''
            if self.volume and self.issue:
                volume = self.volume
                issue = '({}),'.format(self.issue)

            if self.pages:
                if RU == self.language:
                    pages = 'С. {pages},'.format(pages=self.pages)
                else:
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


class Conference(TimeStampedModel):
    """ Conference """
    INTERNATIONAL = 'international'
    NATIONAL = 'national'
    TYPES = (
        (INTERNATIONAL, u'Международная'),
        (NATIONAL, u'Российская')
    )

    ORAL = 'oral'
    POSTER = 'poster'
    TYPES_FORMS = (
        (ORAL, u'Устная'),
        (POSTER, u'Постер')
    )

    type = models.CharField(max_length=25, default=NATIONAL, choices=TYPES, verbose_name=u'Классификация')
    form = models.CharField(max_length=25, default=ORAL, choices=TYPES_FORMS, verbose_name=u'Форма доклада')
    publication = models.OneToOneField(Publication, related_name=u'conference', verbose_name=u'Публикация',
                                       help_text=u'Отсюда берётся название доклада и название конференции: '
                                                 u'статья в сборниках трудов конференции или тезисы конференции')
    author = models.ForeignKey(Author, verbose_name=u'Докладчик')
    organizer = models.CharField(max_length=550, blank=True, verbose_name=u'Организатор')
    date_start = models.DateTimeField(verbose_name=u'Дата и время, начало', help_text=u'Начало конференции')
    date_stop = models.DateTimeField(verbose_name=u'Дата и время, конец', help_text=u'Конец конференции')
    place = models.CharField(max_length=255, verbose_name=u'Место проведения',
                             help_text=u'Например: Страна, город, университет')

    def __unicode__(self):
        return unicode(self.publication.title)

    def name_conference(self):
        return unicode(self.publication.journal)

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'
