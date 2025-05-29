from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaFileViewSet, public_download

router = DefaultRouter()
router.register(r'mediafiles', MediaFileViewSet, basename='mediafile')

urlpatterns = [
    path('', include(router.urls)),
    path('public/<int:pk>/download/', public_download, name='public_download'),
]
