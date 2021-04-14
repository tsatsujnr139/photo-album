from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('photos', views.PhotoViewSet, basename='photo')
router.register('albums', views.PhotoAlbumViewSet, basename='album')

app_name = 'photo_album'

urlpatterns = [
    path('', include(router.urls))
]
