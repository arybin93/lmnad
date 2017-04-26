from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget

from lmnad.models import *
from django.contrib.admin import ModelAdmin
from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin


class AccountForm(ModelForm):
    class Meta:
        widgets = {
            'text': CKEditorWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }

class AccountAdmin(admin.ModelAdmin):
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
            'message': CKEditorWidget(editor_options={'startupFocus': True})
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }


class ProtectionAdmin(ModelAdmin):
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
            'text': CKEditorWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }

class PageAdmin(ModelAdmin):
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
            'text': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text': CKEditorWidget(editor_options={'lang': 'en'}),
            'date': SuitSplitDateTimeWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }

class EventAdmin(ModelAdmin):
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
            'text': CKEditorWidget(editor_options={'lang': 'en'}),
            'full_text': CKEditorWidget(editor_options={'lang': 'en'}),
            'date': SuitSplitDateTimeWidget(),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }

class SeminarAdmin(ModelAdmin):
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

class PeopleAdmin(SortableModelAdmin):
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
            'abstract': RedactorWidget(editor_options={'lang': 'en'})
        }

class ArticleAdmin(ModelAdmin):
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
            'abstract': RedactorWidget(editor_options={'lang': 'en'})
        }

class GrantAdmin(ModelAdmin):
    form = GrantForm
    list_display = ['type', 'number', 'name']
    search_fields = ['name', 'number', 'head']

admin.site.register(Grant, GrantAdmin)

class ProjectForm(ModelForm):
    class Meta:
        widgets = {
            'text': CKEditorWidget(),
            'short_text': CKEditorWidget()
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }

class ProjectAdmin(admin.ModelAdmin):
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
