from django.contrib.auth.models import User
from django.db import models
from constance import config
from django.core.mail import send_mail
from django.template.loader import get_template
from django_extensions.db.models import TimeStampedModel


class Images(TimeStampedModel):
    """ Store restaurant images """
    file = models.ImageField(upload_to='uploads/images', max_length=255, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'

    def __str__(self):
        return self.file.name


class File(models.Model):
    file = models.FileField(upload_to='uploads/lmnad/files', max_length=500,
                            blank=True, null=True, verbose_name='Файл')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name='Персональная страница',
                            help_text='В произвольной форме')
    photo = models.ForeignKey(Images, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'Фото')
    cv_file = models.FileField(upload_to='uploads/users/cv/', null=True, blank=True, verbose_name=u'Файл CV',
                               help_text=u'Прикрепить существующее CV')
    is_subscribe = models.BooleanField(default=True, verbose_name=u'Подписка на email оповещения')

    def __str__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username

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
    fullname = models.CharField(max_length=200, verbose_name='ФИО')
    degree = models.CharField(max_length=50, null=True, blank=True, verbose_name='Степень')
    rank = models.CharField(max_length=50, null=True, blank=True, verbose_name='Учёное звание')
    position = models.CharField(max_length=50, verbose_name='Должность')
    account = models.OneToOneField(Account, models.SET_NULL, blank=True, null=True, verbose_name='Аккаунт сотрудника',
                                   related_name='people', help_text='Если есть')
    science_index = models.TextField(max_length=500, null=True, blank=True, verbose_name='Научный индекс')
    status = models.BooleanField(default=True, verbose_name='Работает')
    date_start = models.DateField(blank=True, null=True, verbose_name='Дата начала работы')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата конца работы')
    order_by = models.PositiveIntegerField(verbose_name='Сортировать', default=0)

    class MPTTMeta:
        order_insertion_by = ['order_by']

    def get_absolute_url(self):
        if self.account:
            return "/profile/{}/".format(self.account.user.username)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Protection(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название работы')
    message = models.TextField(verbose_name='Текст')
    date = models.DateField(blank=True, verbose_name='Дата')
    is_send_email = models.BooleanField(default=False, verbose_name='Сделать рассылку')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            template_text = get_template('lmnad/send_protection_email.txt')
            template_html_text = get_template('lmnad/send_protection_email.html')
            context = {
                'title': self.title,
                'author': self.author,
                'text': self.message,
                'date': self.date
            }

            recipient_list = config.LIST_EMAILS.split(',')
            body_text = template_text.render(context)
            body_html_text = template_html_text.render(context)
            send_mail(
                self.title,
                body_text,
                from_email='lmnad@nntu.ru',
                recipient_list=recipient_list,
                fail_silently=True,
                html_message=body_html_text
            )

        super(Protection, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Защита'
        verbose_name_plural = 'Защиты'


class Page(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название страницы на английском')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


class Grant(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип')
    number = models.CharField(max_length=50, verbose_name='Номер')
    name = models.CharField(max_length=500, verbose_name='Текст')
    head = models.ManyToManyField(People, related_name='head', verbose_name='Руководители')
    members = models.ManyToManyField(People, related_name='members', verbose_name='Участники')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата конца')
    abstract = models.TextField(blank=True, verbose_name='Аннотация')
    reference = models.CharField(max_length=500, blank=True, verbose_name='Ссылка на грант')
    reference_result = models.CharField(max_length=500, blank=True, verbose_name='Cсылка на результаты конкурса')

    def get_absolute_url(self):
        return "/grants/{}/".format(self.number)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Грант'
        verbose_name_plural = 'Гранты'


class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название проекта на английском',
                            help_text='Используется для перехода на страницу')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_text = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    text = models.TextField(verbose_name='Текст')
    link = models.CharField(max_length=100, blank=True, verbose_name='Ссылка на проект')
    is_only_user = models.BooleanField(default=False, verbose_name='Доступно зарегистрированным пользователям')
    images = models.ManyToManyField(Images, blank=True, verbose_name='Изображения',
                                    help_text='Для отображения на странице проекта')
    documents = models.ManyToManyField(File, blank=True, verbose_name='Документы',
                                       help_text='Для доступа на странице проекта')
    order_by = models.PositiveIntegerField(verbose_name='Сортировать', default=0)

    class MPTTMeta:
        order_insertion_by = ['order_by']

    def get_absolute_url(self):
        return "{}/".format(self.name)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Краткое описание')
    full_text = models.TextField(blank=True, verbose_name='Полный текст, отчёт')
    date = models.DateTimeField(verbose_name='Дата и время')
    is_send_email = models.BooleanField(default=False, verbose_name='Сделать рассылку')
    images = models.ManyToManyField(Images, blank=True, verbose_name='Изображения')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            send_email(self.title, self.text, self.date)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "{}/".format(self.pk)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Краткое описание')
    full_text = models.TextField(blank=True, verbose_name='Полный текст, отчёт')
    date = models.DateTimeField(verbose_name='Дата и время')
    is_send_email = models.BooleanField(default=False, verbose_name='Сделать рассылку')

    def save(self, *args, **kwargs):
        if self.is_send_email:
            send_email(self.title, self.text, self.date)
        super(Seminar, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "{}/".format(self.pk)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Семинар'
        verbose_name_plural = 'Семинары'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    authors = models.CharField(max_length=200, verbose_name='Авторы')
    abstract = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Аннотация')
    file = models.FileField(upload_to='uploads/articles/', null=True, blank=True, verbose_name="Файл с тектом статьи")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name='Ссылка')
    source = models.CharField(max_length=200, null=True, blank=True, verbose_name='Журнал, страницы')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время')
    year = models.IntegerField(verbose_name='Год')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '(Old) Статья'
        verbose_name_plural = '(Old) Статьи'


class UsefulLink(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name='Название ссылки, заголовок')
    link = models.URLField(verbose_name='URL Ссылки', help_text='https:/ya.ru')
    order_by = models.PositiveIntegerField(verbose_name='Сортировать', default=0)

    class MPTTMeta:
        order_insertion_by = ['order_by']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Полезная ссылка'
        verbose_name_plural = 'Полезные ссылки'


class Wiki(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(max_length=5000, verbose_name='Текст')
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссылка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Wiki'
        verbose_name_plural = 'Wiki'


def send_email(title, text, date):
    template_text = get_template('lmnad/send_email.txt')
    template_html_text = get_template('lmnad/send_email.html')
    context = {
        'title': title,
        'text': text,
        'date': date
    }

    recipient_list = config.LIST_EMAILS.split(',')
    body_text = template_text.render(context)
    body_html_text = template_html_text.render(context)
    send_mail(
        title,
        body_text,
        from_email='lmnad@nntu.ru',
        recipient_list=recipient_list,
        fail_silently=True,
        html_message=body_html_text
    )
