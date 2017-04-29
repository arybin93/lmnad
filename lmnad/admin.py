from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget

from lmnad.models import *
from django.contrib.admin import ModelAdmin
from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin

from modeltranslation.admin import TranslationAdmin

class AccountForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class AccountAdmin(TranslationAdmin):
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

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ProtectionAdmin(TranslationAdmin):
    list_display = ['author', 'title', 'date']
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

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class PageAdmin(TranslationAdmin):
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

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class EventAdmin(TranslationAdmin):
    list_display = ['title', 'date']
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

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class SeminarAdmin(TranslationAdmin):
    list_display = ['title', 'date']
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

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',)
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class PeopleAdmin(TranslationAdmin, SortableModelAdmin):
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

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ArticleAdmin(TranslationAdmin):
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

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class GrantAdmin(TranslationAdmin):
    form = GrantForm
    list_display = ['type', 'number', 'name']
    search_fields = ['name', 'number', 'head']

admin.site.register(Grant, GrantAdmin)

class ProjectForm(ModelForm):
    class Meta:
        widgets = {
            'text_ru': CKEditorWidget(),
            'short_text_ru': CKEditorWidget(),
            'text_en': CKEditorWidget(),
            'short_text_en': CKEditorWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js',
              'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
              'modeltranslation/js/tabbed_translation_fields.js',
              )
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ProjectAdmin(TranslationAdmin):
    form = ProjectForm
    list_display = ['title']
    suit_form_tabs = (('media', 'Media'),)

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url_thumbnail
        else:
            return ""
    thumbnail.allow_tags = True

admin.site.register(Project, ProjectAdmin)
