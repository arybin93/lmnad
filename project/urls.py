"""project URL Configuration"""
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from igwatlas.views import RecordsViewSet, WaveDataViewSet, SourceViewSet
from igwcoeffs.views import CalculationViewSet
from publications.views import PublicationViewSet

router = routers.DefaultRouter()
router.register('calculation', CalculationViewSet, base_name='calculation')
router.register('publication', PublicationViewSet, base_name='publication')
router.register('records', RecordsViewSet, base_name='records')
router.register('wave_params', WaveDataViewSet, base_name='wave_params')
router.register('sources', SourceViewSet, base_name='sources')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('lmnad.urls')),
    path('', include('igwatlas.urls')),
    path('', include('igwcoeffs.urls')),
    path('', include('publications.urls')),
    path('', include('tank.urls')),
    path('', include('favicon.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('select2/', include('django_select2.urls'))
)
