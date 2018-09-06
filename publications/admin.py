# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import format_html_join, format_html
from django_select2.forms import Select2Widget
from modeltranslation.admin import TabbedTranslationAdmin
from django.db import models
from publications.models import Publication, Author, Journal, AuthorPublication
from django.conf.urls import url

from publications.views import cite_view


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
        'title',
        'year',
        'get_authors',
        'journal',
        'volume',
        'issue',
        'pages',
        'doi',
        'is_rinc',
        'is_wos',
        'is_scopus',
        'is_can_download',
        'is_show',
        'cite'
    ]

    list_filter = [
        'type',
        'year',
        'is_rinc',
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

    def get_urls(self):
        urls = super(PublicationAdmin, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            url(r'^(.+)/cite/$',
                self.admin_site.admin_view(cite_view),
                name='%s_%s_cite' % info)
        ]
        return my_urls + urls

    def get_authors(self, obj):
        result = format_html_join(
            '\n', u"""<li>{}</li>""",
            ((author.get_short_name(),) for author in obj.authors.all())
        )
        return result
    get_authors.short_description = u'Авторы'

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

admin.site.register(Publication, PublicationAdmin)


class AuthorAdmin(TabbedTranslationAdmin):
    list_display = ['last_name', 'name', 'middle_name', 'get_count']
    fields = ['last_name', 'name', 'middle_name']
    search_fields = ['last_name_ru', 'last_name_en']

    def get_count(self, obj):
        return obj.publication_set.count()
    get_count.short_description = u'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    search_fields = ['name_ru', 'name_en']

admin.site.register(Journal, JournalAdmin)
