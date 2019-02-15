# -*- coding: utf-8 -*-
import os

from django.contrib import admin

from django.forms import ModelForm, forms
from django import forms
from django.utils.html import format_html_join
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitSplitDateTimeWidget
from daterange_filter.filter import DateRangeFilter
from igwatlas.models import Record, Source, File, PageData
from django.utils.safestring import mark_safe
from django.conf import settings
from suit_redactor.widgets import RedactorWidget
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from suit_ckeditor.widgets import CKEditorWidget
from django import forms


class RecordForm(ModelForm):
    #new_types = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=Record.TYPES, label='Тип', required=True)

    class Meta:
        model = Record
        exclude = [
            'text',
            'types'    # old types
        ]
        widgets = {
            'date': SuitSplitDateTimeWidget(),
            'date_start': SuitSplitDateTimeWidget(),
            'date_stop': SuitSplitDateTimeWidget(),
            'source': Select2MultipleWidget,
            'file': Select2Widget,
            'new_types': Select2MultipleWidget
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


# IGWAtlas
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_field','position', 'get_types', 'date', 'date_start', 'date_stop', 'get_source']
    form = RecordForm
    search_fields = ['id', 'position', 'image', 'source__source_short', 'source__source']
    list_filter = ['new_types', ('date', RowDateRangeFilter)]
    list_display_links = ['position', 'image_field']

    def get_types(self, obj):
        types = format_html_join(
            '', u"""{}<br>""",
            ((type,) for type in obj.new_types.all())
        )
        return types
    get_types.short_description = 'Типы наблюдений'

    def get_source(self, obj):
        sources = format_html_join(
            '', u"""{}<br>""",
            ((source_obj.source,) for source_obj in obj.source.all())
        )
        return sources
    get_source.short_description = 'Источники'

    def image_field(self, obj):
        return mark_safe("""
            <a target="_blank" href="{}">
            <img src="{}" style="height: 50px;" /></a><br/>
        """.format(obj.image.url, obj.image.url))
    image_field.short_description = 'Изображение'

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
    list_display = ['file']
    search_fields = ['file']

admin.site.register(File, FileAdmin)


class PageDataForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'text_en': CKEditorWidget(editor_options={'lang': 'en'})
        }


class PageDataAdmin(TabbedTranslationAdmin):
    list_display = ['type', 'title']
    form = PageDataForm

admin.site.register(PageData, PageDataAdmin)
