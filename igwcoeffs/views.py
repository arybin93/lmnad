# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from igwcoeffs.api_serializers import CommonSerializer
from igwcoeffs.igw import handle_file
from igwcoeffs.models import Calculation
from constance import config


class CalculationViewSet(viewsets.ViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CommonSerializer

    @list_route(methods=['post'])
    def load_file(self, request):
        """
        Load file
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: form
              type: string
            - name: name
              required: true
              defaultValue:
              description: name of calculation
              paramType: form
              type: string
            - name: file
              required: true
              defaultValue:
              description: File
              paramType: form
              type: file
            - name: separator
              required: true
              defaultValue:
              description: separator for parse
              paramType: form
              type: string
        """
        api_key = request.POST.get('api_key', None)
        name = request.POST.get('name', None)
        separator = request.POST.get('separator', None)
        file = request.FILES['file']
        if api_key and api_key == config.API_KEY_IGWATLAS:
            if file and name and separator:
                status, result, max_row = handle_file(file, separator, max_row=5)
                if status:
                    # create calculation
                    calculation = Calculation.objects.create(name=name,
                                                             source_file=file,
                                                             parse_separator=separator)
                    return Response({"success": status,
                                     'result': result,
                                     'max_row': max_row,
                                     'id': calculation.id})
                else:
                    return Response(CommonSerializer({"success": False, "reason": result, 'message': max_row}).data)
            else:
                return Response(CommonSerializer({"success": False,
                                                  "reason": 'NOT_ENOUGH_PARAMS',
                                                  'message': u'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                              "reason": 'WRONG_API_KEY',
                                              'message': u'Неправильный API KEY'}).data)

    @list_route(methods=['post'])
    def parse_file(self, request):
        """
        Load file
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: form
              type: string
            - name: calc_id
              required: true
              defaultValue:
              description: id of calculation
              paramType: form
              type: string
            - name: parse_field
              required: true
              defaultValue:
              description: Mapping fields
              paramType: form
              type: string
            - name: parse_from
              required: true
              defaultValue: 0
              description: Parse file from
              paramType: form
              type: integer
        """
        api_key = request.POST.get('api_key', None)
        calc_id = request.POST.get('calc_id', None)
        parse_field = request.POST.get('parse_field', None)
        parse_from = request.POST.get('parse_from', None)

        if api_key and api_key == config.API_KEY_IGWATLAS:
            if calc_id and parse_field and parse_from:
                try:
                    calculation = Calculation.objects.get(id=calc_id)
                except Calculation.DoesNotExist:
                    return Response(CommonSerializer({"success": False,
                                                      "reason": 'CALCULATION_NOT_FOUND',
                                                      'message': u'Расчёт не найден'}).data)
                else:
                    calculation.parse_start_from = parse_from
                    calculation.parse_file_fields = parse_field
                    calculation.save()
                    return Response(CommonSerializer({"success": True, "reason": '', 'message': ''}).data)
            else:
                return Response(CommonSerializer({"success": False,
                                                  "reason": 'NOT_ENOUGH_PARAMS',
                                                  'message': u'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                            "reason": 'WRONG_API_KEY',
                                            'message': u'Неправильный API KEY'}).data)

    @list_route(methods=['post'])
    def start_calculation(self):
        """
        Load file
        ---
        parameters_strategy: merge
        parameters:
            - name: api_key
              required: true
              defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
              description: api key access to API
              paramType: form
              type: string
            - name: name
              required: true
              defaultValue:
              description: name of calculation
              paramType: form
              type: string
            - name: file
              required: true
              defaultValue:
              description: File
              paramType: form
              type: file
            - name: separator
              required: true
              defaultValue:
              description: separator for parse
              paramType: form
              type: string
        """
        pass


def igwcoeffs(request):
    """ IGW Coeffs calculator, main page """
    context = {}

    return render(request, 'igwcoeffs/igwcoeffs.html', context)


def igwcoeffs_about(request):
    """ IGW Coeffs calculator, about page """
    context = {}

    return render(request, 'igwcoeffs/about.html', context)
