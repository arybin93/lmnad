from django.db import models
from django.utils.html import format_html

from lmnad.models import Account
from django_extensions.db.models import TimeStampedModel

from lmnad.utils import detect_language_text

RU = 'ru'
EN = 'en'

LANGUAGES = (
    (RU, 'Русский'),
    (EN, 'Английкий')
)


class Journal(TimeStampedModel):
    """ Journal, Conferences """
    JOURNAL = 'journal'
    CONFERENCE = 'conference'
    TYPES = (
        (JOURNAL, 'Журнал'),
        (CONFERENCE, 'Конференция'),
    )

    INTERNATIONAL = 'international'
    NATIONAL = 'national'
    TYPES_CONF = (
        (INTERNATIONAL, 'Международная'),
        (NATIONAL, 'Российская')
    )

    type = models.CharField(max_length=55, default=JOURNAL, choices=TYPES, verbose_name='Тип',
                            help_text='Журнал или конференция')
    name = models.CharField(max_length=255, verbose_name='Название журнала, конференции')

    # Fields for conference
    short_name = models.CharField(max_length=55, verbose_name='Сокращенное название конференции', blank=True)
    conf_type = models.CharField(max_length=25, default=NATIONAL, choices=TYPES_CONF, verbose_name='Классификация')
    date_start = models.DateTimeField(verbose_name='Дата и время, начало', null=True, blank=True,
                                      help_text='Начало конференции')
    date_stop = models.DateTimeField(verbose_name='Дата и время, конец', null=True, blank=True,
                                     help_text='Конец конференции')
    place = models.CharField(max_length=255, blank=True, verbose_name='Место проведения',
                             help_text='Например: Страна, город, университет')
    organizer = models.CharField(max_length=550, blank=True, verbose_name='Организатор')
    description = models.TextField(blank=True, verbose_name='Описание')
    conf_link = models.CharField(max_length=100, blank=True, verbose_name='Ссылка на страницу конференции')
    conf_checkbox = models.BooleanField(default=False, verbose_name="Отображение на странице конференций")

    def __str__(self):
        return self.name

    def get_dates(self):
        date_start = self.date_start.strftime('%d.%m.%Y') if self.date_start else ''
        date_stop = self.date_stop.strftime('%d.%m.%Y') if self.date_stop else ''

        result = '{date_start} - {date_stop}'.format(date_start=date_start,
                                                     date_stop=date_stop)

        return result

    def get_place_dates(self):
        dates = self.get_dates()
        place_and_dates = '{place}, {dates}'.format(place=self.place,
                                                    dates=dates)
        return place_and_dates

    class Meta:
        verbose_name = 'Журнал/Конференция'
        verbose_name_plural = 'Журналы/Конференции'


class Files(TimeStampedModel):
    filename = models.CharField(max_length=255, blank=True, verbose_name="Название файла",
                                help_text="Если поле не заполнено, у документа останется прежнее название")
    file = models.FileField(upload_to='uploads/conference/files', verbose_name='Файл')
    conference = models.ForeignKey(Journal, on_delete=models.CASCADE, verbose_name='Журнал/Конференция',
                                   related_name='files')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.name

    @classmethod
    def name(self):
        return self.file.name.split('/')[-1]


class Author(TimeStampedModel):
    """ Author """
    name = models.CharField(max_length=55, verbose_name='Имя')
    last_name = models.CharField(max_length=55, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=55, blank=True, verbose_name='Отчество')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='author',
                             verbose_name='Пользователь',
                             help_text='Если есть аккаунт')

    def __str__(self):
        full_name = '{} {}'.format(self.last_name, self.name)
        return full_name

    def get_full_name(self):
        if self.middle_name:
            full_name = '{} {} {}'.format(self.last_name, self.name, self.middle_name)
        else:
            full_name = '{} {}'.format(self.last_name, self.name)
        return full_name

    def get_short_name(self):
        short_name = self.name[0]
        if self.middle_name:
            short_middle = self.middle_name[0]
            author_str = "{} {}. {}.".format(self.last_name,
                                             short_name,
                                             short_middle)
        else:
            author_str = "{} {}.".format(self.last_name,
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
            author_str = "{}, {}. {}.".format(last_name,
                                              short_name,
                                              short_middle)
        else:
            author_str = "{}, {}.".format(last_name,
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
        (ARTICLE, 'Статья в периодическом издании'),
        (MONOGRAPH, 'Авторская монография'),
        (GROUP_MONOGRAPH, 'Глава в коллективной монографии'),
        (PROCEEDINGS, 'Статья в сборнике трудов конференции'),
        (THESES_CONFERENCE, 'Тезисы конференции'),
        (TEACHING_MATERIALS, 'Учебно-методические материалы'),
        (PATENT, 'Свидетельство о регистрации права на программный продукт'),
        (PATENT_BD, 'Свидетельство о регистрации права на базу данных')
    )

    type = models.CharField(max_length=55, default=ARTICLE, choices=TYPE, verbose_name='Тип публикации')
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание, аннотация')
    authors = models.ManyToManyField(Author, through='AuthorPublication', verbose_name='Авторы')
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Журнал, конференция')
    year = models.IntegerField(verbose_name='Год')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время')
    volume = models.CharField(max_length=55, blank=True, verbose_name='Том')
    issue = models.CharField(max_length=55, blank=True, verbose_name='Номер журнала/конференции')
    pages = models.CharField(max_length=55, blank=True, verbose_name='Страницы')
    number = models.CharField(max_length=55, blank=True, null=True, verbose_name='Номер свидетельства')
    link = models.CharField(max_length=200, blank=True, verbose_name='Ссылка', help_text='Если есть')
    doi = models.CharField(max_length=200, blank=True, verbose_name='DOI', help_text='Если есть')
    is_rinc = models.BooleanField(default=False, verbose_name='Входит в РИНЦ',
                                  help_text='Отметьте галочку, если публикация входит в РИНЦ')
    is_vak = models.BooleanField(default=False, verbose_name='Входит в ВАК',
                                 help_text='Отметьте галочку, если публикация входит в ВАК')
    is_wos = models.BooleanField(default=False, verbose_name='Входит в WOS',
                                 help_text='Отметьте галочку, если публикация входит в Web of Science')
    is_scopus = models.BooleanField(default=False, verbose_name='Входит в Scopus',
                                    help_text='Отметьте галочку, если публикация входит в Scopus')
    is_other_db = models.BooleanField(default=False, verbose_name='Входит в другие базы данных')
    file = models.FileField(upload_to='uploads/articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    is_can_download = models.BooleanField(default=False, verbose_name='Можно скачать',
                                          help_text='Отметьте галочку, если файл доступен для скачивания')
    is_show = models.BooleanField(default=True, verbose_name='Показывать на сайте',
                                  help_text='Отметьте галочку, чтобы публикация была доступна на сайте')
    language = models.CharField(default=RU, max_length=10, choices=LANGUAGES, verbose_name='Основной язык публикации',
                                help_text='Используется для экпорта/цитирования на сайте в независимости'
                                          ' от выбранного языка на сайте')

    def save(self, *args, **kwargs):
        if not self.language:
            language = detect_language_text(self.title[:30])
            if language == RU:
                self.language = RU
            else:
                self.language = EN
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def information(self):
        """ Get information for publication, use in template """

        if self.type == self.PATENT or self.type == self.PATENT_BD:
            result = format_html(
                '''
                <strong>Номер свидетельства №: </strong> {number} От: {date}
                ''',
                number=self.number,
                date=self.date.strftime('%d.%m.%Y') if self.date else '-'
            )
        else:
            journal = ''
            if self.journal:
                if self.language == RU:
                    journal_name = self.journal.name_ru if self.journal.name_ru else self.journal.name
                else:
                    journal_name = self.journal.name_en if self.journal.name_en else self.journal.name

                if self.journal.type == Journal.CONFERENCE:
                    journal = '{journal_name}, {place}, {dates}'.format(journal_name=journal_name,
                                                                        place=self.journal.place,
                                                                        dates=self.journal.get_dates())
                else:
                    journal = '{},'.format(journal_name)

            issue = ''
            pages = ''
            volume = ''
            if self.volume and self.issue:
                volume = self.volume
                issue = '({}),'.format(self.issue)
            elif self.volume:
                if RU == self.language:
                    volume = 'Т. {volume},'.format(volume=self.volume)
                else:
                    volume = 'vol. {volume},'.format(volume=self.volume)
            elif self.issue:
                if RU == self.language:
                    issue = '№ {issue},'.format(issue=self.issue)
                else:
                    issue = 'no. {issue},'.format(issue=self.issue)

            if self.pages:
                if RU == self.language:
                    pages = 'С. {pages},'.format(pages=self.pages)
                else:
                    pages = 'pp. {pages},'.format(pages=self.pages)

            doi = None
            if self.doi and ('http' not in self.doi or 'https' not in self.doi):
                doi = 'https://doi.org/' + self.doi

            result = format_html(
                '''
                {journal} {volume}{issue} {pages} <strong>DOI: </strong> <a href="{doi_ref}">{doi}</a>
                ''',
                journal=journal,
                volume=volume,
                issue=issue,
                pages=pages,
                doi_ref=doi if doi else self.doi,
                doi=self.doi.replace('https://doi.org/', '') if self.doi else '-',
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
        if self.authors.count():
            authors = self.authors.order_by('authors__order_by')
            if authors.count() > 1:
                len_authors = authors.count() - 1
                authors_list = []
                author_str = ''
                for index, author in enumerate(authors):
                    author_str = '{},'.format(author.get_short_name_harvard(lang=self.language))
                    if index == len_authors:
                        pre_last_author = authors_list[-1]
                        # delete last comma
                        pre_last_author_without_comma = pre_last_author[:-1]
                        authors_list[-1] = pre_last_author_without_comma
                        # last author with &
                        author_str = '& {}'.format(author.get_short_name_harvard(lang=self.language))
                    else:
                        authors_list.append(author_str)

                result_authors = ' '.join(authors_list) + author_str
            else:
                result_authors = '{},'.format(authors.first().get_short_name_harvard(lang=self.language))

        if self.type == self.PATENT or self.type == self.PATENT_BD:
            result = '{authors} {title}. {type_text} {number} от {date}'

            number = self.number if self.number else ''

            if self.type == self.PATENT:
                type_text = 'Свидетельство о государственной регистрации программы для ЭВМ №'
            else:
                type_text = 'Свидетельство о государственной регистрации базы данных №'

            date = self.date.strftime('%d.%m.%Y') if self.date else ''

            return result.format(authors=result_authors,
                                 title=title,
                                 type_text=type_text,
                                 number=number,
                                 date=date)
        else:
            result = '{authors} {year}. {title}. {journal} {volume}{issue} {pages} {doi}'
            doi = 'doi: {}'.format(self.doi) if self.doi else ''

            journal = ''
            if self.journal:
                if self.language == RU:
                    journal_name = self.journal.name_ru if self.journal.name_ru else self.journal.name
                else:
                    journal_name = self.journal.name_en if self.journal.name_en else self.journal.name

                if self.journal.type == Journal.CONFERENCE:
                    journal = '{journal_name}, {place}, {dates},'.format(journal_name=journal_name,
                                                                         place=self.journal.place,
                                                                         dates=self.journal.get_dates())
                else:
                    journal = '{},'.format(journal_name)

            issue = ''
            pages = ''
            volume = ''
            if self.volume and self.issue:
                volume = self.volume
                issue = '({}),'.format(self.issue)
            elif self.volume:
                if RU == self.language:
                    volume = 'Т. {volume},'.format(volume=self.volume)
                else:
                    volume = 'vol. {volume},'.format(volume=self.volume)
            elif self.issue:
                if RU == self.language:
                    issue = '№ {issue},'.format(issue=self.issue)
                else:
                    issue = 'no. {issue},'.format(issue=self.issue)

            if self.pages:
                if RU == self.language:
                    pages = 'С. {pages}'.format(pages=self.pages)
                else:
                    pages = 'pp. {pages}'.format(pages=self.pages)

            if doi and pages:
                pages = '{}, '.format(pages)

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
    author = models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE, verbose_name='Автор')
    publication = models.ForeignKey(Publication, related_name='publications', on_delete=models.CASCADE, verbose_name='Публикация')
    order_by = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения', help_text='От 0 - 100')

    def __str__(self):
        return self.author.last_name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Conference(TimeStampedModel):
    """ Member of conference """

    ORAL = 'oral'
    POSTER = 'poster'
    TYPES_FORMS = (
        (ORAL, 'Устная'),
        (POSTER, 'Постер')
    )

    form = models.CharField(max_length=25, default=ORAL, choices=TYPES_FORMS, verbose_name='Форма доклада')
    publication = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name='conference', verbose_name='Публикация',
                                       help_text='Отсюда берётся название доклада и название конференции: '
                                                 'статья в сборниках трудов конференции или тезисы конференции')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Докладчик')

    def __str__(self):
        result = '{}'.format(self.publication.journal, self.publication.journal.place,)
        return result

    def name_conference(self):
        return self.publication.journal

    class Meta:
        verbose_name = 'Участие в конференции'
        verbose_name_plural = 'Участие в конференциях'
