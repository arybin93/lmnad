# -*- coding: utf-8 -*-
from celery.result import AsyncResult
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from igwcoeffs.api_serializers import CommonSerializer
from igwcoeffs.igw import handle_file, run_calculation
from igwcoeffs.models import Calculation
from constance import config

from lmnad.models import Page
from project.celery import app


class CalculationViewSet(viewsets.ViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CommonSerializer

    @action(detail=False, methods=['post'])
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
                                                  'message': 'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                              "reason": 'WRONG_API_KEY',
                                              'message': 'Неправильный API KEY'}).data)

    @action(detail=False, methods=['post'])
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
                                                      'message': 'Расчёт не найден'}).data)
                else:
                    calculation.parse_start_from = parse_from
                    calculation.parse_file_fields = parse_field
                    calculation.save()
                    return Response({"success": True, 'id': calculation.id})
            else:
                return Response(CommonSerializer({"success": False,
                                                  "reason": 'NOT_ENOUGH_PARAMS',
                                                  'message': 'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                              "reason": 'WRONG_API_KEY',
                                              "message": 'Неправильный API KEY'}).data)

    @action(detail=False, methods=['post'])
    def start_calculation(self, request):
        """
        Start calculation
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
            - name: mode
              required: true
              defaultValue: 1
              description: Mode: 1- first, 2 - second, 0 - both
              paramType: form
              type: string
            - name: email
              required: false
              defaultValue: test@test.com
              description: Send result on email
              paramType: form
              type: string
        """
        api_key = request.POST.get('api_key', None)
        calc_id = request.POST.get('calc_id', None)
        email = request.POST.get('email', None)
        mode = request.POST.get('mode', None)

        if api_key and api_key == config.API_KEY_IGWATLAS:
            if calc_id:
                try:
                    calculation = Calculation.objects.get(id=calc_id)
                except Calculation.DoesNotExist:
                    return Response(CommonSerializer({"success": False,
                                                      "reason": 'CALCULATION_NOT_FOUND',
                                                      'message': 'Расчёт не найден'}).data)
                else:
                    if email:
                        calculation.email = email
                    if mode:
                        calculation.mode = int(mode)
                    calculation.save()

                    # run calculation
                    job = run_calculation.delay(calculation.id)
                    return Response({"success": True, 'job_id': job.id})
            else:
                return Response(CommonSerializer({"success": False,
                                                  "reason": 'NOT_ENOUGH_PARAMS',
                                                  'message': 'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                              "reason": 'WRONG_API_KEY',
                                              "message": 'Неправильный API KEY'}).data)

    @action(detail=False, methods=['get'])
    def status(self, request):
        """
        Get status of calculation
        ---
        parameters_strategy: merge
        parameters:
        - name: api_key
          required: true
          defaultValue: d837d31970deb03ee35c416c5a66be1bba9f56d3
          description: api key access to API
          paramType: query
          type: string
        - name: job_id
          required: true
          defaultValue:
          description: id of job
          paramType: query
          type: string
        """
        api_key = request.GET.get('api_key', None)
        job_id = request.GET.get('job_id', None)

        if api_key and api_key == config.API_KEY_IGWATLAS:
            if job_id:
                res = AsyncResult(job_id, app=app)
                if res.status == 'SUCCESS':
                    status, result = res.get()
                    if status:
                        return Response({"success": True, "result": result})
                    else:
                        return Response(CommonSerializer({"success": False,
                                                          "reason": 'CALCULATION_ERROR',
                                                          "message": 'Ошибка при расчёте'}).data)
                elif res.status == 'FAILURE':
                    return Response({"success": False, "reason": 'ERROR', "message": 'Ошибка'})
                else:
                    return Response({"success": False, "reason": 'IN_PROCESS', "message": 'Расчёт выполняется'})
            else:
                return Response(CommonSerializer({"success": False,
                                                  "reason": 'NOT_ENOUGH_PARAMS',
                                                  'message': 'Не достаточно параметров'}).data)
        else:
            return Response(CommonSerializer({"success": False,
                                              "reason": 'WRONG_API_KEY',
                                              "message": 'Неправильный API KEY'}).data)


def igwcoeffs(request):
    """ IGW Coeffs calculator, main page """
    context = {}

    return render(request, 'igwcoeffs/igwcoeffs.html', context)


def igwcoeffs_about(request):
    """ IGW Coeffs calculator, about page """
    context = {}
    try:
        about_text = Page.objects.get(name='igwcoeffs_about')
    except Page.DoesNotExist:
        pass
    else:
        context['about_text'] = about_text
    return render(request, 'igwcoeffs/about.html', context)
