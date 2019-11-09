# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.forms import ModelForm, forms
from django.http import HttpResponse
from django.utils.html import format_html, format_html_join
from django_select2.forms import Select2MultipleWidget, Select2Widget
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget
from django import forms

from igwatlas.admin import RowDateRangeFilter
from lmnad.models import *
from igwatlas.models import Record, Source
from django.contrib.admin import ModelAdmin
from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin
from datetime import datetime
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from publications.functions import export_grants_to_doc


class MixinModelAdmin:
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget},
    }


class AccountForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
        }


class AccountAdmin(TabbedTranslationAdmin):
    model = Account
    form = AccountForm
    list_display = ['full_name', 'user', 'is_worker', 'is_author']
    search_fields = ['user__username', 'author__last_name']

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Пользователь'

    def is_worker(self, obj):
        if obj.is_worker():
            result = format_html('<img src = "/static/admin/img/icon-yes.svg" alt="True">')
        else:
            result = format_html('<img src = "/static/admin/img/icon-no.svg" alt="False">')
        return result
    is_worker.short_description = 'Является сотрудником'

    def is_author(self, obj):
        if obj.is_author():
            result = format_html('<img src = "/static/admin/img/icon-yes.svg" alt="True">')
        else:
            result = format_html('<img src = "/static/admin/img/icon-no.svg" alt="False">')
        return result
    is_author.short_description = 'Является автором'

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

admin.site.register(Page, PageAdmin)


class EventForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_ru': CKEditorWidget(editor_options={'lang': 'en'}),
            'text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text_en': CKEditorWidget(editor_options={'lang': 'en'}),
            'date': SuitSplitDateTimeWidget(),
            'images': Select2MultipleWidget()
        }


class EventAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'date']
    list_filter = [('date', RowDateRangeFilter)]
    search_fields = ['title']
    form = EventForm


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
            'abstract_en': RedactorWidget(editor_options={'lang': 'en'}),
            'head': Select2MultipleWidget,
            'members': Select2MultipleWidget,
        }


class GrantAdmin(TabbedTranslationAdmin):
    form = GrantForm
    list_display = ['type', 'number', 'name', 'heads', 'date_start', 'date_end']
    fields = [
        'type',
        'number',
        'name',
        'head',
        'members',
        'date_start',
        'date_end',
        'reference',
        'reference_result'
    ]
    search_fields = ['name', 'number']
    list_filter = [('date_start', RowDateRangeFilter)]
    change_list_template = "admin/change_list_export.html"

    def get_urls(self):
        urls = super(GrantAdmin, self).get_urls()
        my_urls = [
            url(r'^export/$', self.admin_site.admin_view(self.export_to_doc),
                name='{}_{}_export'.format(self.model._meta.app_label, self.model._meta.model_name))
        ]
        return my_urls + urls

    def heads(self, obj):
        result = format_html_join(
            '\n', u"""<li>{}</li>""",
            ((head,) for head in obj.head.all())
        )
        return result
    heads.short_description = 'Руководители'

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
        document = export_grants_to_doc(filtered_queryset)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=export_grants_{}.docx'.\
            format(datetime.now().strftime('%d-%m-%Y'))
        document.save(response)
        return response

admin.site.register(Grant, GrantAdmin)


class ProjectForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'short_text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
            'short_text_en': CKEditorWidget(),
            'images': Select2MultipleWidget(),
            'documents': Select2MultipleWidget()
        }


class ProjectAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    form = ProjectForm
    list_display = ['title', 'order_by']
    search_fields = ['title']
    fields = ['name', 'title', 'short_text', 'text', 'link', 'is_only_user', 'images', 'documents']
    sortable = 'order_by'

admin.site.register(Project, ProjectAdmin)


class WikiForm(ModelForm):
    class Meta:
        widgets = {
            'text': CKEditorWidget(),
        }


class WikiAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_link']
    search_fields = ['title']
    form = WikiForm

    def get_link(self, obj):
        return format_html('<a href="{}">{}</a>'.format(obj.link, obj.link))
    get_link.short_description = 'URL'
    get_link.empty_value_display = 'Не указан'

admin.site.register(Wiki, WikiAdmin)


class UsefulLinkAdmin(SortableModelAdmin):
    list_display = ['title', 'get_link', 'order_by']
    search_fields = ['title']
    sortable = 'order_by'

    def get_link(self, obj):
        return format_html('<a href="{}">{}</a>'.format(obj.link, obj.link))
    get_link.short_description = 'URL'
    get_link.empty_value_display = 'Не указан'

admin.site.register(UsefulLink, UsefulLinkAdmin)


admin.site.register(Images)
admin.site.register(File)
