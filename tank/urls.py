from django.urls import path
from rest_framework import routers
from tank.views import tank, tank_exp_detail


router = routers.DefaultRouter()

urlpatterns = [
    path('tank_exp/', tank, name='tank_exp'),
    path('tank_exp/<int:pk>/', tank_exp_detail, name='tank_exp_detail'),
    path('tank_exp_about/', tank, name='tank_exp_about'),
]
