# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
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

    search_fields = ['title', 'doi', 'authors__last_name']
    inlines = [AuthorInline]

    def get_authors(self, obj):
        str = ''
        for author in obj.authors.all():
            short_name = author.name[0] + '. '
            if author.middle_name:
                short_middle = author.middle_name[0]
                author_str = u"{} {}. {}. ;".format(author.last_name,
                                                    short_name,
                                                    short_middle)
            else:
                author_str = u"{} {}. ;".format(author.last_name,
                                                short_name)
            str += author_str
        return str
    get_authors.short_description = u'Авторы'


admin.site.register(Publication, PublicationAdmin)


class AuthorAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'last_name', 'middle_name', 'get_count']
    search_fields = ['last_name']

    def get_count(self, obj):
        return 0
    get_count.short_description = u'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Journal, JournalAdmin)
