# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline

from publications.models import Publication, Author, Journal, AuthorPublication


class AuthorInline(StackedInline):
    model = AuthorPublication
    sortable = 'order_by'
    verbose_name = 'Автор'
    verbose_name_plural = 'Авторы'
    extra = 0


class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        'type',
        'title',
        'get_reference',
        'doi',
        'is_rinc',
        'is_wos',
        'is_scopus',
        'is_can_download',
        'is_show',
        'year'
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

    def get_reference(self, obj):
        str = ', '
        for author in obj.authors.all():
            str += author.last_name
        str += obj.journal.name + ', '+ obj.volume + ', ' + obj.pages
        return str
    get_reference.short_description = u'Источник'


admin.site.register(Publication, PublicationAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'middle_name', 'get_count']
    search_fields = ['last_name']

    def get_count(self, obj):
        return 0
    get_count.short_description = u'Число публикаций'

admin.site.register(Author, AuthorAdmin)


class JournalAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Journal, JournalAdmin)
