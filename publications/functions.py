# -*- coding: utf-8 -*-
from django.db.models import Q
from docx import Document
from docx.shared import Inches
from publications.models import Publication, Conference


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
        filter(Q(is_other_db=True) & Q(Q(is_rinc=False) | Q(is_vak=False) | Q(is_wos=False) | Q(is_scopus=False)))
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


def export_grants_to_doc(queryset):
    document = Document()
    document.add_heading(u'Экспорт грантов', 0)

    for grant in queryset:
        document.add_paragraph(
            grant.export(), style='List Number'
        )

    return document


def export_conference_to_doc(queryset):
    document = Document()
    document.add_heading(u'Экспорт конференций', 0)

    national_conferences = queryset.filter(type=Conference.NATIONAL)
    national_count = national_conferences.count()
    if national_conferences:
        document.add_heading(u'Отечественные мероприятия:', level=2)
        document.add_paragraph(u'- отечественные мероприятия: {}'.format(national_count))

        table = document.add_table(rows=1, cols=3)
        table.style = 'TableGrid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = u'Название мероприятия'
        hdr_cells[1].text = u'Место и время проведения'
        hdr_cells[2].text = u'Название доклада'
        for conf in national_conferences:
            date_start = conf.date_start.strftime('%d.%m.%Y') if conf.date_start else ''
            date_stop = conf.date_stop.strftime('%d.%m.%Y') if conf.date_start else ''
            place_and_dates = u'{place}, {date_start} - {date_stop}'.format(place=conf.place,
                                                                           date_start=date_start,
                                                                           date_stop=date_stop)

            row_cells = table.add_row().cells
            row_cells[0].text = conf.publication.journal.name
            row_cells[1].text = place_and_dates
            row_cells[2].text = conf.publication.title

    international_conferences = queryset.filter(type=Conference.INTERNATIONAL)
    inter_count = international_conferences.count()
    if international_conferences:
        document.add_heading(u'Зарубежные мероприятия:', level=2)
        document.add_paragraph(u'- зарубежные мероприятия: {}'.format(inter_count))

        table = document.add_table(rows=1, cols=3)
        table.style = 'TableGrid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = u'Название мероприятия'
        hdr_cells[1].text = u'Место и время проведения'
        hdr_cells[2].text = u'Название доклада'
        for conf in international_conferences:
            date_start = conf.date_start.strftime('%d.%m.%Y') if conf.date_start else ''
            date_stop = conf.date_stop.strftime('%d.%m.%Y') if conf.date_start else ''
            place_and_dates = u'{place}, {date_start} - {date_stop}'.format(place=conf.place,
                                                                            date_start=date_start,
                                                                            date_stop=date_stop)

            row_cells = table.add_row().cells
            row_cells[0].text = conf.publication.journal.name
            row_cells[1].text = place_and_dates
            row_cells[2].text = conf.publication.title

    return document


def export_from_profile():
    document = Document()
    return document
