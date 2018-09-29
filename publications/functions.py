# -*- coding: utf-8 -*-
from django.db.models import Q
from docx import Document
from docx.shared import Inches
from publications.models import Publication


def export_publication_to_doc(queryset):
    document = Document()
    document.add_heading(u'Экспорт публикаций', 0)
    document.add_heading(u'Статьи в изданиях, рекомендованных ВАК и/или входящих'
                         u' в международные базы цитирования WoS и Scopus:', level=2)
    articles = queryset.filter(type=Publication.ARTICLE).\
        filter(Q(is_rinc=True) | Q(is_vak=True) | Q(is_wos=True) | Q(is_scopus=True))
    for article in articles:
        document.add_paragraph(
            article.get_harvard(), style='List Number'
        )

    document.add_heading(u'Статьи в трудах конференций:', level=2)
    proceedings = queryset.filter(type=Publication.PROCEEDINGS)
    for p in proceedings:
        document.add_paragraph(
            p.get_harvard(), style='List Number'
        )

    document.add_heading(u'Авторские монографии:', level=2)
    mono = queryset.filter(type=Publication.MONOGRAPH)
    for m in mono:
        document.add_paragraph(
            m.get_harvard(), style='List Number'
        )

    document.add_heading(u'Коллективные монографии (глава):', level=2)
    g_mono = queryset.filter(type=Publication.GROUP_MONOGRAPH)
    for gm in g_mono:
        document.add_paragraph(
            gm.get_harvard(), style='List Number'
        )

    document.add_heading(u'Тезисы конференций:', level=2)
    confs = queryset.filter(type=Publication.THESES_CONFERENCE)
    for c in confs:
        document.add_paragraph(
            c.get_harvard(), style='List Number'
        )

    document.add_heading(u'Учебно-методические материалы:', level=2)
    confs = queryset.filter(type=Publication.TEACHING_MATERIALS)
    for c in confs:
        document.add_paragraph(
            c.get_harvard(), style='List Number'
        )

    document.add_heading(u'Прочие статьи:', level=2)
    another_articles = queryset.filter(type=Publication.ARTICLE). \
        filter(Q(is_other_db=True) | Q(Q(is_rinc=False) | Q(is_vak=False) | Q(is_wos=False) | Q(is_scopus=False)))
    for article in another_articles:
        document.add_paragraph(
            article.get_harvard(), style='List Number'
        )

    document.add_heading(u'Авторские свидетельства:', level=2)
    patents = queryset.filter(Q(type=Publication.PATENT) | Q(type=Publication.PATENT_BD))
    for patent in patents:
        document.add_paragraph(
            patent.get_harvard(), style='List Number'
        )

    return document
