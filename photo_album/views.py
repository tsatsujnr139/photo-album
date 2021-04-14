from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from photo_album import serializers
from photo_album.models import PhotoAlbum, Photo


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhotoSerializer
    queryset = Photo.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """returns objects for the authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        """save new photo details"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-photo')
    def upload_image(self, request, pk=None):
        """upload a photo"""
        photo = self.get_object()
        serializer = self.get_serializer(
            photo,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PhotoAlbumViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhotoAlbumSerializer
    queryset = PhotoAlbum.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """returns objects for the authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        """save new photo album details"""
        serializer.save(user=self.request.user)

