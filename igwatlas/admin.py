# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm
from django.utils.html import format_html_join
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitSplitDateTimeWidget
from daterange_filter.filter import DateRangeFilter
from igwatlas.models import Record, Source, File, PageData, WaveData
from django.utils.safestring import mark_safe

from daterange_filter.filter import DateRangeFilter
from modeltranslation.admin import TabbedTranslationAdmin
from suit.widgets import SuitSplitDateTimeWidget
from suit_ckeditor.widgets import CKEditorWidget

from igwatlas.models import Record, Source, File, PageData
from lmnad.models import Account


class RecordForm(ModelForm):
    class Meta:
        model = Record
        exclude = []
        widgets = {
            'date': SuitSplitDateTimeWidget(),
            'date_start': SuitSplitDateTimeWidget(),
            'date_stop': SuitSplitDateTimeWidget(),
            'source': Select2MultipleWidget,
            'file': Select2Widget,
            'new_types': Select2MultipleWidget,
            'user': Select2Widget
        }


class WaveDataForm(ModelForm):

    class Meta:
        model = WaveData
        exclude = []
        widgets = {
            'record': Select2Widget
        }


class WaveDataForm(ModelForm):

    class Meta:
        model = WaveData
        exclude = []
        widgets = {
            'record': Select2Widget
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
    list_display = ['id', 'image_field', 'get_position', 'get_types', 'date', 'date_start', 'date_stop', 'get_source',
                    'is_verified']
    form = RecordForm
    search_fields = ['id', 'position', 'image', 'source__source_short', 'source__source']
    list_filter = ['is_verified', 'new_types', ('date', RowDateRangeFilter)]
    list_display_links = ['get_position', 'image_field']

    def get_position(self, obj):
        latitude = round(float(obj.position.latitude), 3)
        longitude = round(float(obj.position.longitude), 3)
        return '{lat}, {lon}'.format(lat=latitude, lon=longitude)
    get_position.short_description = 'Координаты (Широта, Долгота)'

    def get_types(self, obj):
        types = format_html_join(
            '', u"""{}<br>""",
            ((record_type,) for record_type in obj.new_types.all())
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
        if obj.image:
            return mark_safe("""
                <a target="_blank" href="{}">
                <img src="{}" style="height: 50px;" /></a><br/>
            """.format(obj.image.url, obj.image.url))
        else:
            return 'Нет изображения'
    image_field.short_description = 'Изображение'

    def save_model(self, request, obj, form, change):
        # round coordinates
        latitude = round(float(obj.position.latitude), 3)
        longitude = round(float(obj.position.longitude), 3)
        obj.position = '{lat}, {lon}'.format(lat=latitude, lon=longitude)
        try:
            obj.user = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
        super().save_model(request, obj, form, change)

admin.site.register(Record, RecordAdmin)


class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = '__all__'
        widgets = {
            'files': Select2MultipleWidget,
        }


class SourceAdmin(admin.ModelAdmin):
    list_display = ['source_short', 'link', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['source_short', 'source']
    form = SourceForm

    def save_model(self, request, obj, form, change):
        try:
            obj.user = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
        super().save_model(request, obj, form, change)

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


class WaveDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'record', 'type', 'mode', 'amplitude', 'period', 'polarity']
    form = WaveDataForm
    search_fields = ['id', 'type', 'mode', 'amplitude', 'period', 'polarity']
    list_filter = ['type', 'mode', 'polarity']
    list_display_links = ['id']


admin.site.register(WaveData, WaveDataAdmin)
