from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, VideoViewSet
router = DefaultRouter()
router.register('images', ImageViewSet)
router.register('videos', VideoViewSet)

# ============================================================
# router.register('posts', PostViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
