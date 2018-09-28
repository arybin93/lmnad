# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import format_html_join, format_html
from django_select2.forms import Select2Widget
from modeltranslation.admin import TabbedTranslationAdmin
from django.db import models

from publications.functions import export_publication_to_doc
from publications.models import Publication, Author, Journal, AuthorPublication
from django.conf.urls import url

from publications.views import cite_view
from datetime import datetime


class MixinModelAdmin:
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget},
    }


class AuthorInline(MixinModelAdmin, StackedInline):
    model = AuthorPublication
    sortable = 'order_by'
    verbose_name = 'Автор'
    verbose_name_plural = 'Авторы'
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
    inlines = [AuthorInline]
    change_list_template = "admin/change_list_export.html"

    def get_urls(self):
        urls = super(PublicationAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            url(r'^(.+)/cite/$',
                self.admin_site.admin_view(cite_view),
                name='%s_%s_cite' % info),
            url(r'^export/$', self.admin_site.admin_view(self.export_to_doc), name='%s_%s_export' % info)
        ]
        return my_urls + urls

    def get_authors(self, obj):
        result = format_html_join(
            '\n', u"""<li>{}</li>""",
            ((author.get_short_name(),) for author in obj.authors.all())
        )
        return result
    get_authors.short_description = u'Авторы'

    def get_information(self, obj):
        if obj.type == Publication.PATENT or obj.type == Publication.PATENT_BD:
            result = format_html(
                u'''
                <strong>Номер свидетельства №: </strong> {} <br>
                <strong>От: </strong> {} <br>
                ''',
                obj.number,
                obj.date.strftime('%d.%m.%Y') if obj.date else u'-'
            )
        else:
            doi = None
            if 'http' not in obj.doi or 'https' not in obj.doi:
                doi = 'https://doi.org/' + obj.doi

            result = format_html(
                u'''
                <strong>Журнал: </strong> {} <br>
                <strong>Том: </strong> {} <br>
                <strong>Номер журнала: </strong> {} <br>
                <strong>Страницы: </strong> {} <br>
                <strong>DOI: </strong> <a href="{}">{}</a> <br>
                ''',
                obj.journal,
                obj.volume if obj.volume else u'-',
                obj.issue if obj.issue else u'-',
                obj.pages if obj.pages else u'-',
                doi if doi else obj.doi,
                obj.doi.replace('https://doi.org/', '') if obj.doi else u'',
            )

        return result
    get_information.short_description = u'Источник'

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
    cite.short_description = u'Ссылка'

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
    get_count.short_description = u'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    search_fields = ['name_ru', 'name_en']

admin.site.register(Journal, JournalAdmin)
