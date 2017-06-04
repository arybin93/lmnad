# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.forms import ModelForm, forms
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitSplitDateTimeWidget

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

# IGWAtlas
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'position', 'get_types']
    form = RecordForm
    list_filter = []

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
    form = SourceForm

admin.site.register(Source, SourceAdmin)

admin.site.register(File)
