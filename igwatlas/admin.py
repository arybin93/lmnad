# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.forms import ModelForm, forms
from django import forms
from django_select2.forms import Select2MultipleWidget
from suit.widgets import SuitSplitDateTimeWidget

from igwatlas.models import Record, Source

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
            'source': Select2MultipleWidget
        }

# IGWAtlas
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'position']
    form = RecordForm

admin.site.register(Record, RecordAdmin)

class SourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
