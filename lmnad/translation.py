from modeltranslation.translator import translator, TranslationOptions
from lmnad.models import *


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'short_text', 'text')

translator.register(Project, ProjectTranslationOptions)


class AccountTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(Account, AccountTranslationOptions)


class PeopleTranslationOptions(TranslationOptions):
    fields = ('fullname', 'degree', 'rank', 'position', )

translator.register(People, PeopleTranslationOptions)


class ProtectionTranslationOptions(TranslationOptions):
    fields = ('author', 'title', 'message',)

translator.register(Protection, ProtectionTranslationOptions)


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)

translator.register(Page, PageTranslationOptions)


class GrantTranslationOptions(TranslationOptions):
    fields = ('type', 'name', 'abstract',)

translator.register(Grant, GrantTranslationOptions)


class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'full_text',)


translator.register(Event, EventTranslationOptions)


class SeminarTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'full_text',)

translator.register(Seminar, SeminarTranslationOptions)


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'authors', 'abstract', 'source')

translator.register(Article, ArticleTranslationOptions)
