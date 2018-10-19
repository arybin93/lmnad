# Core Django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max, Min
from django.db.models import Q
from django.shortcuts import render

# Third-party app imports
from rest_framework import viewsets
from rest_framework.response import Response
from constance import config

# Imports from our apps
from igwatlas.models import Record, Source, PageData
from igwatlas.api_serializers import RecordSerializer, SourceSerializer
from lmnad.models import Project


class RecordsViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def list(self, request):
        """
        List of records objects for Yandex map
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: query
              type: string
            - name: types
              required: false
              defaultValue: 0,1,2
              description: types of observations
              paramType: query
              type: string
            - name: date_from
              required: false
              defaultValue: 1987-12-24
              description: get records from date
              paramType: query
              type: string
            - name: date_to
              required: false
              defaultValue: 2017-12-24
              description: get records to date
              paramType: query
              type: string
            - name: source_text
              required: false
              defaultValue: Christopher R. Jackson, 2004
              description: get records by source
              paramType: query
              type: string
        """
        api_key = request.GET.get('api_key', None)
        types = request.GET.get('types', None)
        date_from = request.GET.get('date_from', None)
        date_to = request.GET.get('date_to', None)
        source_text = request.GET.get('source_text', None)

        if api_key and api_key == config.API_KEY_IGWATLAS:
            records = Record.objects.all()

            if types:
                records = records.filter(types__icontains=types)

            if date_from and date_to:
                records = records.filter(Q(date__gte=date_from) & Q(date__lte=date_to))
            elif date_from:
                records = records.filter(date__gte=date_from)
            elif date_to:
                records = records.filter(date__lte=date_to)

            if source_text:
                records = records.filter(source__source__icontains=source_text)

            result_object = {
                'type': 'FeatureCollection',
                'features': []
            }
            for record in records:
                lat = record.position.latitude
                lon = record.position.longitude

                short_text_source = ''
                full_text_source = ''
                link_text_source = ''
                for source in record.source.all():
                    short_text_source += source.source_short + ';'
                    full_text_source += source.source + ';'
                    if source.link:
                        link_text_source += source.link + ';'

                date = ''
                if record.date:
                    date = record.date.strftime('%d-%m-%Y')

                img = ''
                if record.image:
                    img = (
                        '<a target="_blank" href="{}">'
                        '<img src="{}" style="height: 50px;" /></a><br/> '.format(
                            record.image.url,
                            record.image.url
                        )
                    )

                obj = {
                    'type': 'Feature',
                    'id': record.id,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lat, lon]
                    },
                    'properties': {
                        'hintContent': short_text_source + str(record.position),
                        'balloonContentHeader': record.get_text_types(),
                        'balloonContentBody': full_text_source + "<br>" + img + "<br>" + str(record.position),
                        'balloonContentFooter': link_text_source + ' ' + date,
                        'clusterCaption': record.get_text_types()
                    }
                }
                result_object['features'].append(obj)

            return Response(result_object)
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def list(self, request):
        """
        List of records objects for Yandex map
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: query
              type: string
            - name: query
              required: false
              defaultValue: Christopher R. Jackson, 2004
              description: get records by source
              paramType: query
              type: string
        """
        api_key = request.GET.get('api_key', None)
        query = request.GET.get('query', None)

        if api_key and api_key == config.API_KEY_IGWATLAS:

            if query:
                sources_list = Source.objects.filter(Q(source_short__icontains=query) | Q(source__icontains=query))
            else:
                sources_list = Source.objects.all()

            page = request.GET.get('page', 1)
            paginator = Paginator(sources_list, 15)

            try:
                sources = paginator.page(page)
            except PageNotAnInteger:
                sources = paginator.page(1)
            except EmptyPage:
                sources = paginator.page(paginator.num_pages)

            return Response(sources)
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})


def igwatlas(request):
    """ IGW Atlas main page """
    context = {}

    try:
        page_data_map = PageData.objects.get(type=PageData.MAP_TEXT)
    except PageData.DoesNotExist:
        pass
    else:
        context['page_data_map'] = page_data_map

    try:
        page_data_graphic = PageData.objects.get(type=PageData.GRAPHIC_TEXT)
    except PageData.DoesNotExist:
        pass
    else:
        context['page_data_graphic'] = page_data_graphic

    try:
        page_data_satellite = PageData.objects.get(type=PageData.SATELLITE_TEXT)
    except PageData.DoesNotExist:
        pass
    else:
        context['page_data_satellite'] = page_data_satellite

    try:
        page_data_table = PageData.objects.get(type=PageData.TABLE_TEXT)
    except PageData.DoesNotExist:
        pass
    else:
        context['page_data_table'] = page_data_table

    try:
        page_data_record = PageData.objects.get(type=PageData.RECORD_TEXT)
    except PageData.DoesNotExist:
        pass
    else:
        context['page_data_record'] = page_data_record

    sources_count = Source.objects.all().count()
    observation_count = Record.objects.all().count()

    min_date = Record.objects.all().aggregate(Min('date'))
    max_date = Record.objects.all().aggregate(Max('date'))

    context['min_date'] = min_date['date__min']
    context['max_date'] = max_date['date__max']
    context['count_observation'] = observation_count
    context['count_sources'] = sources_count
    context['project'] = Project.objects.get(name='igwatlas_online')

    return render(request, 'igwatlas/igwatlas.html', context)


def yandex_map(request):
    """ IGW Atlas yandex map page and search """
    context = {
        'project': Project.objects.get(name='igwatlas_online')
    }
    return render(request, 'igwatlas/map.html', context)


def source(request):
    """ IGW Atlas table of source page """
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if query:
        sources_list = Source.objects.filter(Q(source_short__icontains=query) | Q(source__icontains=query))
    else:
        sources_list = Source.objects.all()

    paginator = Paginator(sources_list, 15)

    try:
        sources = paginator.page(page)
    except PageNotAnInteger:
        sources = paginator.page(1)
    except EmptyPage:
        sources = paginator.page(paginator.num_pages)

    context = {
        'sources': sources,
        'project': Project.objects.get(name='igwatlas_online')
    }
    return render(request, 'igwatlas/sources.html', context)


def about(request):
    context = {}

    try:
        igwatlas_about = PageData.objects.get(type=PageData.ABOUT_TEXT)
    except PageData.DoesNotExist:
        context['error'] = 'Создайте данные для страницы'
    else:
        context['igwatlas_about'] = igwatlas_about
        context['project'] = Project.objects.get(name='igwatlas_online')

    return render(request, 'igwatlas/about.html', context)
