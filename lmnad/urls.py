from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^people/$', views.people, name='people'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^seminars/$', views.seminars, name='seminars'),
    url(r'^seminars/(?P<pk>.*)?/$', views.seminar_detail),
    url(r'^protections/$', views.protections, name='protections'),
    url(r'^grants/$', views.grants, name='grants'),
    url(r'^grants/(?P<number>.*)?/$', views.grants_detail),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<name>.*)?/$', views.project_detail),
    url(r'^events/$', views.events, name='events'),
    url(r'^events/(?P<pk>.*)?/$', views.event_detail),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^profile/(?P<username>.*)?/$', views.profile, name='profile'),
    url(r'^profile_export/(?P<username>.*)?/$', views.profile_export, name='profile_export'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^pages/(?P<name>.*)?$', views.pages, name='pages')
]