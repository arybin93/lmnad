# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.forms import ModelForm, forms
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitSplitDateTimeWidget
from daterange_filter.filter import DateRangeFilter

from igwatlas.models import Record, Source, File

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
            'file': Select2Widget
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
    list_display = ['id', 'position', 'get_types', 'date', 'date_start', 'date_stop']
    form = RecordForm
    search_fields = ['position']
    list_filter = [RecordTypeFilter, ('date', RowDateRangeFilter)]

    def get_types(self, obj):
        return obj.get_text_types()
    get_types.short_description = u'Типы наблюдений'

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
