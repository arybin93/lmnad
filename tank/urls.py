from django.conf.urls import url, include
from rest_framework import routers
from tank.views import  *

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^tank/', tank, name='tank'),
]
