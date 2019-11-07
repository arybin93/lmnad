import django_filters
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from publications.models import Publication
from publications.serializers import PublicationSerializer


def publications(request):
    """ Publications """
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if query:
        try:
            year = int(query)
            publications_qs = Publication.objects.filter(is_show=True, year=year).order_by('-year')
        except ValueError:
            publications_qs = Publication.objects.filter(is_show=True).filter(Q(title__icontains=query) |
                                                         Q(journal__name__icontains=query) |
                                                         Q(authors__last_name__icontains=query) |
                                                         Q(authors__name__icontains=query) |
                                                         Q(doi__icontains=query)).order_by('-year').distinct()
    else:
        publications_qs = Publication.objects.filter(is_show=True).order_by('-year')

    paginator = Paginator(publications_qs, 25)
    try:
        publications_obj = paginator.page(page)
    except PageNotAnInteger:
        publications_obj = paginator.page(1)
    except EmptyPage:
        publications_obj = paginator.page(paginator.num_pages)

    context = {
        'publications': publications_obj
    }

    return render(request, 'publications/page.html', context)


def publications_search(request):
    """ Publications search """
    year_from = request.GET.get('year_from', None)
    year_to = request.GET.get('year_to', None)
    types = request.GET.getlist('type', [])
    author = request.GET.get('author', None)
    enable_checkbox = request.GET.get('enable_checkbox', False)
    rinc = request.GET.get('rinc', False)
    vak = request.GET.get('vak', False)
    wos = request.GET.get('wos', False)
    scopus = request.GET.get('scopus', False)

    publications_qs = Publication.objects.filter(is_show=True).order_by('-year')

    if year_from and year_to:
        publications_qs = publications_qs.filter(year__gte=int(year_from), year__lte=int(year_to))
    elif year_to:
        publications_qs = publications_qs.filter(year__lte=int(year_to))
    elif year_from:
        publications_qs = publications_qs.filter(year__gte=int(year_from))

    if author:
        publications_qs = publications_qs.filter(Q(authors__last_name_ru__icontains=author) |
                                                 Q(authors__last_name_en__icontains=author))

    if types:
        publications_qs = publications_qs.filter(type__in=types)

    if enable_checkbox == 'on':
        if rinc and rinc == 'on':
            is_rinc = True
        else:
            is_rinc = False

        if vak and vak == 'on':
            is_vak = True
        else:
            is_vak = False

        if wos and wos == 'on':
            is_wos = True
        else:
            is_wos = False

        if scopus and scopus == 'on':
            is_scopus = True
        else:
            is_scopus = False

        publications_qs = publications_qs.filter(Q(is_rinc=is_rinc) &
                                                 Q(is_vak=is_vak) &
                                                 Q(is_wos=is_wos) &
                                                 Q(is_scopus=is_scopus))

    context = {
        'publications': publications_qs
    }

    return render(request, 'publications/page.html', context)


def cite_view(request, obj_id):
    template = 'admin/cite.html'

    publication = get_object_or_404(Publication, pk=obj_id)

    context = {
        'harvard': publication.get_harvard(),
        'is_popup': True
    }
    return TemplateResponse(request, template, context)


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = PageNumberPagination

