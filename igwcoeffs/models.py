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
        (TYPE_POINT, 'Расчёт для одной точки'),
        (TYPE_SECTION, 'Расчёт для разреза')
    )

    BOTH_MODES = 0
    FIRST_MODE = 1
    SECOND_MODE = 2
    MODE_TYPES = (
        (BOTH_MODES, 'Двух мод'),
        (FIRST_MODE, 'Первой моды'),
        (SECOND_MODE, 'Второй моды')
    )

    SPACE = ' '
    SLASH = '/'
    COMMA = ','
    SEMICOLON = ';'

    SEPARATORS = (
        (SPACE, 'Пробел'),
        (SLASH, '/'),
        (COMMA, ','),
        (SEMICOLON, ';')
    )

    name = models.CharField(max_length=255, verbose_name='Название расчёта')
    source_file = models.FileField(upload_to='uploads/igwcoeffs/sources', max_length=255,
                                   verbose_name='Файл с исходными данными')
    result_file = models.FileField(upload_to='uploads/igwcoeffs/results', max_length=255,
                                   verbose_name='Файл с результатом', blank=True, null=True)
    types = models.PositiveIntegerField(default=TYPE_POINT, choices=TYPES, verbose_name='Тип расчёта')
    mode = models.PositiveIntegerField(default=FIRST_MODE, choices=MODE_TYPES, verbose_name='Расчёт для')
    email = models.CharField(max_length=55, blank=True, verbose_name='Email',
                             help_text='Для отправки результата расчёта на почту')
    parse_start_from = models.PositiveIntegerField(default=0, verbose_name='Считать файл с', help_text='Номер строки')
    parse_file_fields = models.CharField(max_length=255, blank=True, verbose_name='Соответствие полей')
    parse_separator = models.CharField(max_length=10, default=SPACE, choices=SEPARATORS, verbose_name='Разделитель')

    class Meta:
        verbose_name = 'Расчёт'
        verbose_name_plural = 'Расчёты'

    def __str__(self):
        return self.name
