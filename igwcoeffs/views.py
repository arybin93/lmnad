# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from igwcoeffs.api_serializers import CommonSerializer
from igwcoeffs.models import Calculation


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
            - name: file
              required: true
              defaultValue:
              description: File
              paramType: form
              type: file
        """
        print request
        # handle file
        # response list of data from file, first 5 row
        return Response(CommonSerializer({"success": True, "reason": '', 'message': ''}).data)


def igwcoeffs(request):
    """ IGW Coeffs calculator, main page """
    context = {}

    return render(request, 'igwcoeffs/igwcoeffs.html', context)


def igwcoeffs_about(request):
    """ IGW Coeffs calculator, about page """
    context = {}

    return render(request, 'igwcoeffs/about.html', context)
