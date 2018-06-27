from django.conf.urls import url, include
from rest_framework import routers
from igwatlas.views import igwatlas, yandex_map, source, about, RecordsViewSet, SourceViewSet


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^igwatlas/$', igwatlas, name='igwatlas'),
    url(r'^igwatlas_map/$', yandex_map , name='map'),
    url(r'^igwatlas_source/$', source, name='source'),
    url(r'^igwatlas_about/$', about, name='about'),
]
