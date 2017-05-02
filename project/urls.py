"""project URL Configuration"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/$', RedirectView.as_view(url='lmnad/article/')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('lmnad.urls')),
    url(r'^', include('favicon.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^select2/', include('django_select2.urls')),
)
