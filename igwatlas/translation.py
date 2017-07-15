from modeltranslation.translator import translator, TranslationOptions
from igwatlas.models import *

class PageDataTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

translator.register(PageData, PageDataTranslationOptions)
