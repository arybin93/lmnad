# -*- coding: utf-8 -*-
import os

from django.contrib import admin

from django.forms import ModelForm, forms
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitSplitDateTimeWidget
from daterange_filter.filter import DateRangeFilter
from igwatlas.models import Record, Source, File, PageData
from django.utils.safestring import mark_safe
from django.conf import settings
from suit_redactor.widgets import RedactorWidget
from modeltranslation.admin import TranslationAdmin
from suit_ckeditor.widgets import CKEditorWidget


# widgets
class AdminImageWidget(forms.ClearableFileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 50px;" /></a><br/> '
                           % (value.url, value.url)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class RecordForm(ModelForm):
    types = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=Record.TYPES,
                                         label=u'Тип', required=True)
    class Meta:
        model = Record
        fields = '__all__'
        widgets = {
            'date': SuitSplitDateTimeWidget(),
            'date_start': SuitSplitDateTimeWidget(),
            'date_stop': SuitSplitDateTimeWidget(),
            'source': Select2MultipleWidget,
            'file': Select2Widget,
            'image': AdminImageWidget
        }


# filters
class RowDateRangeFilter(DateRangeFilter):
    template = 'admin/daterange_filter.html'

    def choices(self, changelist):
        yield {
            'selected': False,
            'query_string': "",
            'display': 'All',
        }


class RecordTypeFilter(admin.SimpleListFilter):
    title = 'Тип наблюдения'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        MAP = 0
        GRAPHIC = 1
        SATELLITE = 2
        RECORD = 3
        TABLE = 4
        return (
            (MAP, u'Карта'),
            (GRAPHIC, u'График'),
            (SATELLITE, u'Спутниковый снимок'),
            (RECORD, u'Запись'),
            (TABLE, u'Таблица')
        )

    def queryset(self, request, queryset):
        Record.objects.filter()
        if self.value():
            queryset = queryset.filter(types__icontains=self.value())

        return queryset


# IGWAtlas
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_field', 'position', 'get_types', 'date', 'date_start', 'date_stop']
    form = RecordForm
    search_fields = ['position', 'image', 'source__source_short', 'source__source']
    list_filter = [RecordTypeFilter, ('date', RowDateRangeFilter)]
    list_display_links = ['position', 'image_field']

    def get_types(self, obj):
        return obj.get_text_types()
    get_types.short_description = u'Типы наблюдений'

    def image_field(self, obj):
        if obj.image and os.path.isfile(obj.image.path):
            img = u'<img src="{0}/{1}" style="max-height: 100px;"/>'.format(settings.MEDIA_URL, obj.image)
            return img
        else:
            return obj.image
    image_field.short_description = u'Изображение'
    image_field.allow_tags = True

admin.site.register(Record, RecordAdmin)


class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = '__all__'
        widgets = {
            'files': Select2MultipleWidget,
        }


class SourceAdmin(admin.ModelAdmin):
    list_display = ['source_short', 'link']
    search_fields = ['source_short', 'source']
    form = SourceForm

admin.site.register(Source, SourceAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ['path', 'file']
    search_fields = ['path', 'file']

admin.site.register(File, FileAdmin)


class PageDataForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'text_en': CKEditorWidget(editor_options={'lang': 'en'})
        }

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class PageDataAdmin(TranslationAdmin):
    list_display = ['type', 'title']
    form = PageDataForm

admin.site.register(PageData, PageDataAdmin)
