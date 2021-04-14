from rest_framework import serializers

from photo_album.models import Photo, PhotoAlbum


class PhotoSerializer(serializers.ModelSerializer):
    """serializer for photos"""

    class Meta:
        model = Photo
        fields = ('id', 'title', 'created', 'updated',)
        read_only_fields = ('id',)


class PhotoAlbumSerializer(serializers.ModelSerializer):
    """serializer for photo album"""
    photos = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())

    class Meta:
        model = PhotoAlbum
        fields = ('id', 'title', 'photos', 'created', 'updated',)
        read_only_fields = ('id',)
