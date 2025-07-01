from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import MediaFileViewSet, public_download

router = DefaultRouter()
router.register(r'mediafiles', MediaFileViewSet, basename='mediafile')
=======
from .views import MediaFileViewSet, public_download, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'mediafiles', MediaFileViewSet, basename='mediafile')
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a

urlpatterns = [
    path('', include(router.urls)),
    path('public/<int:pk>/download/', public_download, name='public_download'),
]
