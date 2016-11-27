from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^people/$', views.people, name='people'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^seminars/$', views.seminars, name='seminars'),
    url(r'^protections/$', views.protections, name='protections'),
    url(r'^igwresearch/$', views.igwresearch, name='igwresearch'),
    url(r'^events/$', views.events, name='events'),
    url(r'^contacts/$', views.contacts, name='contacts'),
]