from django.urls import path

from . import views

urlpatterns = [
    path('publications/', views.publications, name='publications'),
    path('publications_search/', views.publications_search, name='publications_search'),
    path('publications/cite/<int:obj_id>', views.cite_view, name='cite'),
]