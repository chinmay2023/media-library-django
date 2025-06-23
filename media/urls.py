from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaFileViewSet, public_download, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'mediafiles', MediaFileViewSet, basename='mediafile')
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('public/<int:pk>/download/', public_download, name='public_download'),
]
