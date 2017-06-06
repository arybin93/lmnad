from django.conf.urls import url, include
from rest_framework import routers
from igwatlas.views import RecordViewSet, SourceViewSet, FileViewSet
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='IGWAtlas API')

router = routers.DefaultRouter()
router.register(r'records', RecordViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^docs$', schema_view)
]
