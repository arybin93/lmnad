from django.urls import path
from igwatlas.views import igwatlas, yandex_map, source, about, yandex_map_params
from rest_framework_swagger.views import get_swagger_view


swagger_docs_view = get_swagger_view(title='LMNAD API')

urlpatterns = [
    path('docs/', swagger_docs_view),
    path('igwatlas/', igwatlas, name='igwatlas'),
    path('igwatlas_map/', yandex_map, name='map'),
    path('igwatlas_params/', yandex_map_params, name='parameters'),
    path('igwatlas_source/', source, name='source'),
    path('igwatlas_about/', about, name='about'),
]
