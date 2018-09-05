from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publications/$', views.publications, name='publications'),
]