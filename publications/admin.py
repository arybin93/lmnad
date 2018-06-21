# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.utils.html import format_html_join
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from publications.models import Publication, Author, Journal, AuthorPublication


class AuthorInline(StackedInline):
    model = AuthorPublication
    sortable = 'order_by'
    verbose_name = 'Автор'
    verbose_name_plural = 'Авторы'
    extra = 0


class PublicationAdmin(TabbedTranslationAdmin):
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

    search_fields = ['title_ru', 'title_en', 'doi', 'authors__last_name', 'journal__name']
    inlines = [AuthorInline]

    def get_authors(self, obj):
        result = format_html_join(
            '\n', u"""<li>{}</li>""",
            ((author.get_short_name(),) for author in obj.authors.all())
        )
        return result
    get_authors.short_description = u'Авторы'


admin.site.register(Publication, PublicationAdmin)


class AuthorAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'last_name', 'middle_name', 'get_count']
    search_fields = ['last_name_ru', 'last_name_en']

    def get_count(self, obj):
        return 0
    get_count.short_description = u'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    search_fields = ['name_ru', 'name_en']

admin.site.register(Journal, JournalAdmin)
