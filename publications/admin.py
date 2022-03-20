# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.admin import TabularInline
from django.forms import ModelForm, forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import format_html_join, format_html
from django_select2.forms import Select2Widget
from modeltranslation.admin import TabbedTranslationAdmin
from django.db import models
from suit.widgets import SuitSplitDateTimeWidget
from suit_ckeditor.widgets import CKEditorWidget

from igwatlas.admin import RowDateRangeFilter
from publications.functions import export_publication_to_doc, export_conference_to_doc
from publications.models import Publication, Author, Journal, AuthorPublication, Conference, Files
from django.conf.urls import url

from publications.views import cite_view
from datetime import datetime


class MixinModelAdmin:
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget},
        models.OneToOneField: {'widget': Select2Widget},
        models.TextField: {'widget': CKEditorWidget(editor_options={'startupFocus': True})},
    }


class DateTimeSelectMixin:
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }


class AuthorInline(MixinModelAdmin, TabularInline):
    model = AuthorPublication
    fields = ['author', 'order_by']
    sortable = 'order_by'
    verbose_name = 'Автор'
    verbose_name_plural = 'Авторы'
    extra = 5


class ConferenceInline(MixinModelAdmin, TabularInline):
    model = Conference
    fields = [
        'author',
        'form',
    ]
    verbose_name = 'Участие в конференции'
    verbose_name_plural = 'Участие в конференции'
    max_num = 1
    extra = 1


class PublicationAdmin(MixinModelAdmin, TabbedTranslationAdmin):
    list_display = [
        'type',
        'get_authors',
        'title',
        'get_information',
        'is_rinc',
        'is_vak',
        'is_wos',
        'is_scopus',
        'is_can_download',
        'is_show',
        'year',
        'cite'
    ]

    list_filter = [
        'type',
        'year',
        'is_rinc',
        'is_vak',
        'is_wos',
        'is_scopus',
        'is_can_download',
        'is_show'
    ]

    search_fields = [
        'title_ru',
        'title_en',
        'doi',
        'authors__last_name_ru',
        'authors__last_name_en',
        'journal__name_ru',
        'journal__name_en'
    ]
    inlines = [ConferenceInline, AuthorInline]
    change_list_template = "admin/change_list_export.html"

    def get_urls(self):
        urls = super(PublicationAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/cite/$',
                self.admin_site.admin_view(cite_view),
                name='{}_{}_cite'.format(self.model._meta.app_label, self.model._meta.model_name)),
            url(r'^export/$', self.admin_site.admin_view(self.export_to_doc),
                name='{}_{}_export'.format(self.model._meta.app_label, self.model._meta.model_name))
        ]
        return my_urls + urls

    def get_authors(self, obj):
        result = format_html_join(
            '\n', """<li>{}</li>""",
            ((author.get_short_name(),) for author in obj.authors.all())
        )
        return result
    get_authors.short_description = 'Авторы'

    def get_information(self, obj):
        if obj.type == Publication.PATENT or obj.type == Publication.PATENT_BD:
            result = format_html(
                '''
                <strong>Номер свидетельства №: </strong> {} <br>
                <strong>От: </strong> {} <br>
                ''',
                obj.number,
                obj.date.strftime('%d.%m.%Y') if obj.date else '-'
            )
        else:
            doi = None
            if 'http' not in obj.doi or 'https' not in obj.doi:
                doi = 'https://doi.org/' + obj.doi

            result = format_html(
                '''
                <strong>Журнал/Конференция: </strong> {} <br>
                <strong>Том: </strong> {} <br>
                <strong>Номер журнала: </strong> {} <br>
                <strong>Страницы: </strong> {} <br>
                <strong>DOI: </strong> <a href="{}">{}</a> <br>
                ''',
                obj.journal if obj.journal else '-',
                obj.volume if obj.volume else '-',
                obj.issue if obj.issue else '-',
                obj.pages if obj.pages else '-',
                doi if doi else obj.doi,
                obj.doi.replace('https://doi.org/', '') if obj.doi else '',
            )

        return result
    get_information.short_description = 'Источник'

    def cite(self, obj):
        result = format_html(
            u"""
            <a onclick="return showAddAnotherPopup(this);"
            href="{}/cite/"
            class="btn btn-primary custom">Получить</a>
            """,
            obj.id
        )
        return result
    cite.short_description = 'Ссылка'

    def export_to_doc(self, request, **kwargs):
        ChangeList = self.get_changelist(request)
        cl = ChangeList(request,
                        self.model,
                        self.list_display,
                        self.list_display_links,
                        self.list_filter,
                        self.date_hierarchy,
                        self.search_fields,
                        self.list_select_related,
                        self.list_per_page,
                        self.list_max_show_all,
                        self.list_editable,
                        self)

        filtered_queryset = cl.get_queryset(request)
        document = export_publication_to_doc(filtered_queryset)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=export_{}.docx'.\
            format(datetime.now().strftime('%d-%m-%Y'))
        document.save(response)
        return response

    class Media:
        js = ('admin/publications.js',)

admin.site.register(Publication, PublicationAdmin)


class AuthorAdmin(MixinModelAdmin, TabbedTranslationAdmin):
    list_display = ['last_name', 'name', 'middle_name', 'get_count']
    fields = ['last_name', 'name', 'middle_name', 'user']
    search_fields = ['last_name_ru', 'last_name_en']

    def get_count(self, obj):
        return obj.publication_set.count()
    get_count.short_description = 'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = "__all__"
        widgets = {
            'description': CKEditorWidget(),
        }

    def clean(self):
        if self.cleaned_data['type'] == Journal.CONFERENCE:
            if 'date_start' in self.cleaned_data or 'date_stop' in self.cleaned_data:
                if not self.cleaned_data['date_start'] or not self.cleaned_data['date_stop']:
                    raise forms.ValidationError('Выберите даты проведения конференции')

            if 'place' in self.cleaned_data:
                if not self.cleaned_data['place']:
                    raise forms.ValidationError('Введите место проведения конференции')

        return super(JournalForm, self).clean()

    class Media:
        js = ('admin/journals.js',)


class FilesInline(StackedInline):
    model = Files
    extra = 0


class JournalAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    list_filter = ['type', 'conf_type']
    search_fields = ['name_ru', 'name_en']
    inlines = [FilesInline]
    form = JournalForm

admin.site.register(Journal, JournalAdmin)


class ConferenceForm(ModelForm):
    class Meta:
        model = Conference
        fields = [
            'form',
            'publication',
            'author',
        ]
        widgets = {
            'date_start': SuitSplitDateTimeWidget(),
            'date_stop': SuitSplitDateTimeWidget(),
        }


class ConferenceAdmin(MixinModelAdmin, admin.ModelAdmin):
    list_display = [
        'get_name_conference',
        'get_conf_type',
        'publication',
        'author',
        'get_dates'
    ]
    list_filter = ['form', ('publication__journal__date_start', RowDateRangeFilter)]
    search_fields = [
        'author__last_name_ru',
        'author__last_name_en',
        'publication__journal__name_ru',
        'publication__journal__name_en'
    ]
    form = ConferenceForm
    change_list_template = "admin/change_list_export.html"

    def get_urls(self):
        urls = super(ConferenceAdmin, self).get_urls()
        my_urls = [
            url(r'^export/$', self.admin_site.admin_view(self.export_to_doc),
                name='{}_{}_export'.format(self.model._meta.app_label, self.model._meta.model_name))
        ]
        return my_urls + urls

    def get_name_conference(self, obj):
        return obj.publication.journal
    get_name_conference.short_description = 'Название конференции'

    def get_dates(self, obj):
        return obj.publication.journal.get_dates()
    get_dates.short_description = 'Даты'

    def get_conf_type(self, obj):
        return obj.publication.journal.get_conf_type_display()
    get_conf_type.short_description = 'Тип конференции'

    def get_place(self, obj):
        return obj.publication.journal.place
    get_place.short_description = 'Место'

    def export_to_doc(self, request, **kwargs):
        ChangeList = self.get_changelist(request)
        cl = ChangeList(request,
                        self.model,
                        self.list_display,
                        self.list_display_links,
                        self.list_filter,
                        self.date_hierarchy,
                        self.search_fields,
                        self.list_select_related,
                        self.list_per_page,
                        self.list_max_show_all,
                        self.list_editable,
                        self)

        filtered_queryset = cl.get_queryset(request)
        document = export_conference_to_doc(filtered_queryset)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=export_conferences_{}.docx'. \
            format(datetime.now().strftime('%d-%m-%Y'))
        document.save(response)
        return response

admin.site.register(Conference, ConferenceAdmin)
