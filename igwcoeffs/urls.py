from django.urls import path
from igwcoeffs.views import igwcoeffs, igwcoeffs_about


urlpatterns = [
    path('igwcoeffs/', igwcoeffs, name='igwcoeffs'),
    path('igwcoeffs_about/', igwcoeffs_about, name='igwcoeffs_about')
]
