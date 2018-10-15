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
    url(r'^user/(?P<username>[\w-]+)/export/publication/$', views.profile_export, name='export_publication'),
    url(r'^user/(?P<username>[\w-]+)/add/publication/$', views.profile_add_publication, name='add_publication'),
    url(r'^user/(?P<username>[\w-]+)/edit/publication/(?P<id>\d+)/$', views.profile_edit_publication,
        name='edit_publication'),
    url(r'^user/(?P<username>[\w-]+)/cancel/$', views.profile_cancel, name='profile_cancel'),
    url(r'^user/(?P<username>[\w-]+)/add/journal/$', views.profile_add_journal, name='add_journal'),
    url(r'^user/(?P<username>[\w-]+)/add/author/$', views.profile_add_author, name='add_author'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^pages/(?P<name>.*)?$', views.pages, name='pages')
]