from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^publications/cite/(?P<obj_id>.*)?$', views.cite_view, name='cite'),
]