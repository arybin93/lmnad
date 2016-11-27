from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from lmnad.models import *
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = True
    verbose_name_plural = 'accounts'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProtectionAdmin(MarkdownModelAdmin):
    list_display = ['author', 'title', 'message', 'date']
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(Protection, ProtectionAdmin)

class PageAdmin(MarkdownModelAdmin):
    list_display = ['name','title', 'text']
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(Page, PageAdmin)

class EventAdmin(MarkdownModelAdmin):
    list_display = ['title', 'text', 'date']
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(Event, EventAdmin)

class SeminarAdmin(MarkdownModelAdmin):
    list_display = ['title', 'text', 'date']
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(Seminar, SeminarAdmin)


class PeopleAdmin(MarkdownModelAdmin):
    list_display = ['fullname', 'degree', 'position']

admin.site.register(People, PeopleAdmin)

class ArticleAdmin(MarkdownModelAdmin):
    list_display = ['authors', 'abstract','link','source','date','year']

admin.site.register(Article, ArticleAdmin)