from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^publications_search/$', views.publications_search, name='publications_search'),
    url(r'^publications/cite/(?P<obj_id>.*)?$', views.cite_view, name='cite'),
]