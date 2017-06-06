from django.shortcuts import render
from rest_framework import viewsets
from api_serializers import RecordSerializer, FileSerializer, SourceSerializer
from igwatlas.models import Record, Source, File


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
