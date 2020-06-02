from django.db import models

from geoposition.fields import GeopositionField
from igwcoeffs.models import TimeStampedModel
from lmnad.models import Account


class File(models.Model):
    path = models.CharField(max_length=500, blank=True, verbose_name='Название файла, путь',
                            help_text='uploads/igwatlas/sources/')
    file = models.FileField(upload_to='uploads/igwatlas/sources', max_length=500,
                            blank=True, null=True, verbose_name='Файл')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
    def __str__(self):
        if self.file:
            return self.file.name
        else:
            return self.path


# IGWAtlas
class Source(models.Model):
    source_short = models.CharField(max_length=255, verbose_name='Краткое описание')
    source = models.TextField(verbose_name='Описание')
    files = models.ManyToManyField(File, blank=True, verbose_name='Файлы для источника',
                                   help_text='Один источник может быть представлен в нескольких файлах')
    link = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name='Ссылка', help_text='Если есть')
    is_verified = models.BooleanField(default=True, verbose_name='Проверено',
                                      help_text='Поставьте галочку, если источник проверен')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='source',
                             verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.source_short


class RecordType(models.Model):
    name = models.CharField(max_length=55, unique=True, verbose_name='Название типа записи')
    value = models.PositiveIntegerField(default=0, unique=True, verbose_name=u'Цифровое значение для типа')

    def __str__(self):
        return self.name


class Record(TimeStampedModel):
    MAP = 0
    GRAPHIC = 1
    SATELLITE = 2
    RECORD = 3
    TABLE = 4

    TYPES = (
        (MAP, 'Карта'),
        (GRAPHIC, 'График'),
        (SATELLITE, 'Спутниковый снимок'),
        (RECORD, 'Запись'),
        (TABLE, 'Таблица')
    )

    position = GeopositionField(verbose_name='Координаты')
    new_types = models.ManyToManyField(RecordType, verbose_name='Тип', help_text='Поддерживается несколько типов')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время наблюдения')
    date_start = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время начала наблюдений',
                                      help_text='Если есть')
    date_stop = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время конца наблюдений',
                                     help_text='Если есть')
    image = models.ImageField(upload_to='uploads/igwatlas/images', verbose_name='Изображение')
    source = models.ManyToManyField(Source, verbose_name='Источник')
    page = models.CharField(max_length=15, blank=True, null=True, verbose_name='Страницы из источника')
    text = models.TextField(blank=True, null=True, verbose_name='Описание для наблюдения')
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name='Файл, источник изображения',
                             help_text='Если источник представлен одним файлом, данное поле можно не заполнять')

    is_verified = models.BooleanField(default=True, verbose_name='Проверено',
                                      help_text='Поставьте галочку, если запись проверена')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='records',
                             verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Наблюдение'
        verbose_name_plural = 'Наблюдения'

    def __str__(self):
        return self.image.name

    def get_text_types(self):
        text = ''
        for record_type in self.new_types.all():
            text += record_type.name + '; '
        return text


class PageData(models.Model):
    MAP_TEXT = 0
    GRAPHIC_TEXT = 1
    SATELLITE_TEXT = 2
    RECORD_TEXT = 3
    TABLE_TEXT = 4
    ABOUT_TEXT = 5

    TYPES = (
        (MAP_TEXT, 'Текст о типе: карта'),
        (GRAPHIC_TEXT, 'Текст о типе: график'),
        (SATELLITE_TEXT, 'Текст о типе: спутник'),
        (RECORD_TEXT, 'Текст о типе: запись'),
        (TABLE_TEXT, 'Текст о типе: таблица'),
        (ABOUT_TEXT, 'Текст о проекте'),
    )

    type = models.PositiveIntegerField(default=MAP_TEXT, choices=TYPES, unique=True,
                                       verbose_name='Тип данных, страницы')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Данные для страниц'
        verbose_name_plural = 'Данные для страниц'


class WaveData(models.Model):
    LONG_WAVES = 0
    INTERNAL_BORE = 1
    SHORT_PERIOD = 2

    TYPES = (
        (LONG_WAVES, 'Длинные волны'),
        (INTERNAL_BORE, 'Внутренний бор'),
        (SHORT_PERIOD, 'Короткопериодные волны'),
     )

    DEFAULT_MODE = 1

    type = models.PositiveIntegerField(default=SHORT_PERIOD, choices=TYPES, unique=True,
                                       verbose_name='Тип ВВ')
    mode = models.PositiveIntegerField(default=DEFAULT_MODE, verbose_name='Мода ВВ')
    amplitude = models.FloatField(verbose_name='Амплитуда ВВ в метрах')
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='Запись для анализа')

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'
