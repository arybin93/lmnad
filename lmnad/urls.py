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
    url(r'^contacts/$', views.contactView, name='contacts'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^profile/(?P<username>.*)?/$', views.profile),
    url(r'^edit/$', views.EditProfileView, name='edit_profile'),
]