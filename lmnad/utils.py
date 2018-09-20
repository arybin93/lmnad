# -*- coding: utf-8 -*-
from django.conf import settings
from yandex_translate import YandexTranslate


def detect_language_text(text):
    translate = YandexTranslate(settings.YANDEX_TRANSLATE_API_KEY)
    part_text = text[1:50]
    return translate.detect(part_text)
