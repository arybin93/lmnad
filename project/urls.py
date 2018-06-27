"""project URL Configuration"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers

from igwatlas.views import RecordsViewSet, SourceViewSet
from igwcoeffs.views import CalculationViewSet

router = routers.DefaultRouter()
router.register(r'calculation', CalculationViewSet, base_name='calculation')
router.register(r'records', RecordsViewSet, base_name='records')
router.register(r'sources', SourceViewSet, base_name='sources')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/$', RedirectView.as_view(url='lmnad/event/')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('lmnad.urls')),
    url(r'^', include('igwatlas.urls')),
    url(r'^', include('igwcoeffs.urls')),
    url(r'^', include('tank.urls')),
    url(r'^', include('favicon.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^select2/', include('django_select2.urls'))
)
