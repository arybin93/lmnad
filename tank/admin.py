# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms import ModelForm
from suit.widgets import SuitSplitDateTimeWidget
from tank.models import Experiment, Movie, Data, Images


class RecordForm(ModelForm):
    class Meta:
        model = Experiment
        fields = '__all__'
        widgets = {
            'date': SuitSplitDateTimeWidget(),
        }


class MovieInline(StackedInline):
    model = Movie
    extra = 0


class ImagesInline(StackedInline):
    model = Images
    extra = 0


class DataInline(StackedInline):
    model = Data
    extra = 0


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    search_fields = ['name']
    list_filter = ['date']
    inlines = [MovieInline, ImagesInline, DataInline]
    form = RecordForm

admin.site.register(Experiment, ExperimentAdmin)
