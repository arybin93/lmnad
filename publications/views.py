from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from rest_framework import viewsets

from publications.models import Publication


def publications(request):
    """ Publications """
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if query:
        try:
            year = int(query)
            publications_qs = Publication.objects.filter(is_show=True, year=year).order_by('-year')
        except ValueError:
            publications_qs = Publication.objects.filter(Q(title__icontains=query) |
                                                         Q(journal__name__icontains=query) |
                                                         Q(authors__last_name__icontains=query) |
                                                         Q(authors__name__icontains=query)).order_by('-year')
    else:
        publications_qs = Publication.objects.filter(is_show=True).order_by('-year')

    paginator = Paginator(publications_qs, 25)
    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)

    context = {
        'publications': publications
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


class PublicationViewSet(viewsets.ViewSet):
    pass
