from modeltranslation.translator import translator, TranslationOptions
from publications.models import Publication, Journal, Author


class PublicationTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Publication, PublicationTranslationOptions)


class JournalTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Journal, JournalTranslationOptions)


class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'last_name', 'middle_name')

translator.register(Author, AuthorTranslationOptions)