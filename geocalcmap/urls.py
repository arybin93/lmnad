from django.urls import path

from . import views

urlpatterns = [
    path('geocalcmap', views.index, name='index'),
]