# -*- coding: utf-8 -*-

# Stdlib imports
from __future__ import unicode_literals
import os

# Core Django imports
from django.db.models import Max, Min
from django.shortcuts import render

# Third-party app imports
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from constance import config

# Imports from our apps
from igwatlas.models import Record, Source, File, PageData
from api_serializers import RecordSerializer, FileSerializer, SourceSerializer
from django.conf import settings


class RecordsViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @list_route(methods=['get'])
    def get_records(self, request):
        """
        Get records objects for Yandex map
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: query
              type: string
        """
        api_key = request.GET.get('api_key', None)
        if api_key and api_key == config.API_KEY_IGWATLAS:
            records = self.queryset

            result_object = {
                'type': 'FeatureCollection',
                'features': []
            }
            for record in records:
                lat = record.position.latitude
                lon = record.position.longitude

                short_text_source = ''
                full_text_source = ''
                for source in record.source.all():
                    short_text_source += source.source_short + ';'
                    full_text_source += source.source + ';'

                date = ''
                if record.date:
                    date = record.date.strftime('%d-%m-%Y')

                img = ''
                if record.image:
                    img = ('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 50px;" /></a><br/> '
                           % (record.image.url, record.image.url))

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
                        'balloonContentFooter': date,
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

    return render(request, 'igwatlas/igwatlas.html', context)

def yandex_map(request):
    """ IGW Atlas yandex map page and search """
    context = {}
    return render(request, 'igwatlas/map.html', context)

def source(request):
    """ IGW Atlas table of source page """
    context = {}
    return render(request, 'igwatlas/sources.html', context)

def about(request):
    context = {}

    try:
        igwatlas_about = PageData.objects.get(type=PageData.ABOUT_TEXT)
    except PageData.DoesNotExist:
        context['error'] = u'Создайте данные для страницы'
    else:
        context['igwatlas_about'] = igwatlas_about

    return render(request, 'igwatlas/about.html', context)
