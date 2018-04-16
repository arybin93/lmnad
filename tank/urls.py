from django.conf.urls import url, include
from rest_framework import routers
from tank.views import  *

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^tank_exp/$', tank, name='tank_exp'),
    url(r'^tank_exp/(?P<pk>.*)?/$', tank_exp_detail),
    url(r'^tank_exp_about/', tank, name='tank_exp_about'),
]
