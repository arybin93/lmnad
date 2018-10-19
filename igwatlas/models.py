from django.db import models
from geoposition.fields import GeopositionField
import re


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
            return self.file
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

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.source_short


class Record(models.Model):
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
    types = models.TextField(verbose_name='Тип', help_text='Поддерживается несколько типов')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время наблюдения')
    date_start = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время начала наблюдений',
                                      help_text='Если есть')
    date_stop = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время конца наблюдений',
                                     help_text='Если есть')
    image = models.ImageField(upload_to='uploads/igwatlas/images', blank=True, verbose_name='Изображение')
    source = models.ManyToManyField(Source, verbose_name='Источник')
    page = models.CharField(max_length=15, blank=True, null=True, verbose_name='Страницы из источника')
    data = models.FileField(upload_to='uploads/igwatlas/data', null=True, blank=True,
                            verbose_name='Оцифрованные данные', help_text=u'Если есть')
    text = models.TextField(blank=True, null=True, verbose_name='Описание для наблюдения')
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name='Файл, источник изображения',
                             help_text='Если источник представлен одним файлом, данное поле можно не заполнять')

    class Meta:
        verbose_name = 'Наблюдение'
        verbose_name_plural = 'Наблюдения'

    def __str__(self):
        return self.position

    def get_text_types(self):
        text = ''
        # numbers
        reg_number = re.compile(r'(\d+)')
        types_list = []
        for r in reg_number.findall(self.types):
            types_list.append(r)

        type_dict = self.get_types()

        for type in types_list:
            index = int(type)
            text = text + type_dict[index] + '; '

        return text

    @staticmethod
    def get_types():
        types = {}
        for i in Record.TYPES:
            types.update({
                i[0]: i[1]
            })
        return types


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

    type = models.PositiveIntegerField(default=MAP_TEXT, choices=TYPES, unique=True, verbose_name='Тип данных, страницы')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Данные для страниц'
        verbose_name_plural = 'Данные для страниц'
