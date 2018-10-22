from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('people/', views.people, name='people'),
    path('articles/', views.articles, name='articles'),
    path('seminars/', views.seminars, name='seminars'),
    path('seminars/<int:pk>/', views.seminar_detail),
    path('protections/', views.protections, name='protections'),
    path('grants/', views.grants, name='grants'),
    path('grants/<str:number>/', views.grants_detail),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:name>/', views.project_detail),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('user/<slug:username>/export/publication/', views.profile_export, name='export_publication'),
    path('user/<slug:username>/add/publication/', views.profile_add_publication, name='add_publication'),
    path('user/<slug:username>/edit/publication/<int:id>/', views.profile_edit_publication, name='edit_publication'),
    path('user/<slug:username>/cancel/', views.profile_cancel, name='profile_cancel'),
    path('user/<slug:username>/add/journal/', views.profile_add_journal, name='add_journal'),
    path('user/<slug:username>/add/author/', views.profile_add_author, name='add_author'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('pages/<slug:name>', views.pages, name='pages')
]
