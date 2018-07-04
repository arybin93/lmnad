# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm, forms
from django_select2.forms import Select2MultipleWidget
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget
from django import forms

from igwatlas.admin import RowDateRangeFilter
from lmnad.models import *
from igwatlas.models import Record, Source
from django.contrib.admin import ModelAdmin
from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


class AccountForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
        }


class AccountAdmin(TabbedTranslationAdmin):
    model = Account
    form = AccountForm
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""
    thumbnail.allow_tags = True

admin.site.register(Account, AccountAdmin)


class ProtectionForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'message_ru': CKEditorWidget(editor_options={'startupFocus': True}),
            'message_en': CKEditorWidget(editor_options={'startupFocus': True})
        }


class ProtectionAdmin(TranslationAdmin):
    list_display = ['author', 'title', 'date']
    list_filter = [('date', RowDateRangeFilter)]
    search_fields = ['title']
    form = ProtectionForm
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""

    thumbnail.allow_tags = True

admin.site.register(Protection, ProtectionAdmin)


class PageForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
        }


class PageAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'title']
    form = PageForm
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""

    thumbnail.allow_tags = True


admin.site.register(Page, PageAdmin)


class EventForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'date': SuitSplitDateTimeWidget(),
        }


class EventAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'date']
    list_filter = [('date', RowDateRangeFilter)]
    search_fields = ['title']
    form = EventForm
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""

    thumbnail.allow_tags = True

admin.site.register(Event, EventAdmin)


class SeminarForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'date': SuitSplitDateTimeWidget(),
        }


class SeminarAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'date']
    list_filter = [('date', RowDateRangeFilter)]
    search_fields = ['title']
    fields = ['title', 'text', 'date', 'is_send_email']
    form = SeminarForm
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""

    thumbnail.allow_tags = True

admin.site.register(Seminar, SeminarAdmin)


class PeopleForm(ModelForm):
    class Meta:
        model = People
        fields = '__all__'
        widgets = {
            'date_start': SuitDateWidget(),
            'date_end': SuitDateWidget(),
            'science_index': RedactorWidget(editor_options={'lang': 'en'})
        }


class PeopleAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = ['fullname', 'degree', 'rank', 'position', 'order_by', 'status']
    list_filter = ['status']
    list_editable = ('status',)
    search_fields = ['fullname']
    form = PeopleForm
    sortable = 'order_by'

admin.site.register(People, PeopleAdmin)


class ArticleForm(ModelForm):
    class Meta:
        widgets = {
            'abstract_ru': RedactorWidget(editor_options={'lang': 'en'}),
            'abstract_en': RedactorWidget(editor_options={'lang': 'en'})
        }


class ArticleAdmin(TabbedTranslationAdmin):
    list_display = ['authors', 'title', 'source', 'year']
    search_fields = ['authors', 'title', 'year']
    form = ArticleForm

admin.site.register(Article, ArticleAdmin)


class GrantForm(ModelForm):
    class Meta:
        model = Grant
        fields = '__all__'
        widgets = {
            'date_start': SuitDateWidget(),
            'date_end': SuitDateWidget(),
            'abstract_ru': RedactorWidget(editor_options={'lang': 'en'}),
            'abstract_en': RedactorWidget(editor_options={'lang': 'en'})
        }


class GrantAdmin(TabbedTranslationAdmin):
    form = GrantForm
    list_display = ['type', 'number', 'name', 'date_start', 'date_end']
    search_fields = ['name', 'number', 'head']
    list_filter = ['date_start', 'date_end']

admin.site.register(Grant, GrantAdmin)


class ProjectForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'short_text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
            'short_text_en': CKEditorWidget()
        }


class ProjectAdmin(TabbedTranslationAdmin):
    form = ProjectForm
    list_display = ['title']
    fields = ['name', 'title', 'short_text', 'text', 'link', 'is_only_user']
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""
    thumbnail.allow_tags = True

admin.site.register(Project, ProjectAdmin)


class WikiForm(ModelForm):
    class Meta:
        widgets = {
            'text': CKEditorWidget(),
        }


class WikiAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    form = WikiForm

admin.site.register(Wiki, WikiAdmin)
