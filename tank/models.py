import os
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


class Experiment(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Эксперимент'
        verbose_name_plural = 'Эксперименты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/tank_exp/{}/".format(self.id)


class Movie(TimeStampedModel):
    file = models.FileField(upload_to='uploads/tank/movies', verbose_name='Запись', help_text='Видео, гифка')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='Эксперимент',
                                   related_name='movies')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.file.name


class Images(TimeStampedModel):
    """ Store restaurant images """
    file = models.ImageField(upload_to='uploads/tank/images', max_length=255, verbose_name='Фото')
    is_schema = models.BooleanField(default=False, verbose_name='Cхема эксперимента', help_text='Да, нет')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='Эксперимент',
                                   related_name='images')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return self.file.name

    def filename(self):
        return os.path.basename(self.file.name)


class Data(TimeStampedModel):
    file = models.FileField(upload_to='uploads/tank/data', verbose_name='Данные')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='Эксперимент',
                                   related_name='data')

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'

    def __str__(self):
        return self.file.name

    @classmethod
    def name(self):
        return self.file.name.split('/')[-1]
