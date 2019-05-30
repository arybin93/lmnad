# Core Django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max, Min
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token

# Third-party app imports
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from constance import config

# Imports from our apps
from igwatlas.models import Record, Source, PageData, RecordType, File
from igwatlas.api_serializers import RecordSerializer, SourceSerializer, RecordYandexSerializer
from lmnad.models import Project


class YandexObject:
    def __init__(self, type, features):
        self.type = type
        self.features = features


def authenticate(api_key=None):
    if not api_key:
        return

    try:
        token = Token.objects.get(key=api_key)
    except Token.DoesNotExist:
        return

    return token.user


class RecordsViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request):
        """
        List of records
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: query
              type: string
            - name: is_yandex_map
              required: false
              defaultValue: 1
              description: return objects for yandex map
              paramType: query
              type: boolean
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
            - name: limit
              required: false
              defaultValue: 100
              description: limit for records
              paramType: query
              type: integer
            - name: offset
              required: false
              defaultValue: 0
              description: offset for records
              paramType: query
              type: integer
        """
        api_key = request.GET.get('api_key', None)
        is_yandex_map = int(request.GET.get('is_yandex_map', 1))
        types = request.GET.get('types', None)
        date_from = request.GET.get('date_from', None)
        date_to = request.GET.get('date_to', None)
        source_text = request.GET.get('source_text', None)
        # TODO: params for rectangle zone: two points

        user = authenticate(api_key)
        if api_key and (api_key == config.API_KEY_IGWATLAS or user):
            records = Record.objects.filter(is_verified=True)

            if types:
                types_lst = types.rstrip(',').split(',')
                records = records.filter(new_types__value__in=types_lst)

            if date_from and date_to:
                records = records.filter(Q(date__gte=date_from) & Q(date__lte=date_to))
            elif date_from:
                records = records.filter(date__gte=date_from)
            elif date_to:
                records = records.filter(date__lte=date_to)

            if source_text:
                records = records.filter(source__source__icontains=source_text)

            page_records = self.paginate_queryset(records)
            if page_records is None:
                page_records = records

            if is_yandex_map:
                result = RecordYandexSerializer(YandexObject(type='FeatureCollection', features=page_records)).data
            else:
                result = RecordSerializer(page_records, many=True, context={'request': request}).data

            return self.get_paginated_response(result)
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})

    def create(self, request):
        api_key = request.POST.get('api_key', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        types = request.POST.get('types', None)
        date = request.POST.get('date', None)
        date_start = request.POST.get('date_start', None)
        date_stop = request.POST.get('date_stop', None)
        image = request.FILES.get('image', None)
        source_id = request.POST.get('source', None)
        page = request.POST.get('page', None)

        user = authenticate(api_key)
        if api_key and (api_key == config.API_KEY_IGWATLAS or user):

            if not latitude and not longitude:
                return Response({"success": False, 'reason': 'NOT_COORDINATES'})

            if not types:
                return Response({"success": False, 'reason': 'NOT_TYPE'})

            if not image:
                return Response({"success": False, 'reason': 'NOT_IMAGE'})

            if not source_id:
                return Response({"success": False, 'reason': 'NOT_SOURCE'})

            try:
                source_obj = Source.objects.get(id=source_id)
            except Source.DoesNotExist:
                return Response({"success": False, 'reason': 'SOURCE_NOT_FOUND'})

            types_lst = types.split(',')
            type_list_obj = []
            for type_str in types_lst:
                try:
                    type = RecordType.objects.get(value=type_str)
                except RecordType.DoesNotExist:
                    return Response({"success": False, 'reason': 'RECORD_TYPE_NOT_FOUND'})
                else:
                    type_list_obj.append(type)
            longitude = round(float(longitude), 3)
            latitude = round(float(latitude), 3)

            position = '{}, {}'.format(latitude, longitude)
            new_record = Record.objects.create(position=position, image=image, page=page, is_verified=False,
                                               date=date, date_start=date_start, date_stop=date_stop, user=user)

            for type in type_list_obj:
                new_record.new_types.add(type)

            new_record.source.add(source_obj)
            new_record.save()
            return Response({"success": True})
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})



    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class SourceViewSet(viewsets.ViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = LimitOffsetPagination

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

            page_sources = self.paginate_queryset(sources_list)
            if page_sources is None:
                page_sources = sources_list

            result = SourceSerializer(page_sources, many=True, context={'request': request}).data

            return self.get_paginated_response(result)
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})

    def retrieve(self, request, pk=None):
        api_key = request.GET.get('api_key', None)
        if api_key and api_key == config.API_KEY_IGWATLAS:
            queryset = Source.objects.all()
            source = get_object_or_404(queryset, pk=pk)
            return Response(SourceSerializer(source).data)
        else:
            return Response({"success": False, 'reason': 'WRONG_API_KEY'})

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def create(self, request):
        api_key = request.POST.get('api_key', None)
        source_short = request.POST.get('source_short', None)
        source = request.POST.get('source', None)
        files = request.FILES.getlist('files', None)
        link = request.POST.get('link', None)

        user = authenticate(api_key)
        if api_key and (api_key == config.API_KEY_IGWATLAS or user):
            if not source_short:
                return Response({"success": False, 'reason': 'NOT_SHORT_SOURCE'})

            if not source:
                return Response({"success": False, 'reason': 'NOT_SOURCE'})

            if not files:
                return Response({"success": False, 'reason': 'NOT_FILE'})

            file_list_obj = []
            for file in files:
                new_file = File.objects.create(file=file)
                file_list_obj.append(new_file)

            new_source = Source.objects.create(source_short=source_short, source=source, is_verified=False,
                                               link=link, user=user)
            for new_file in file_list_obj:
                new_source.files.add(new_file)

            return Response({"success": True, 'source_id': new_source.id})
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
