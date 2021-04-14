import tempfile
import os
import pytest
from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from photo_album.models import Photo, PhotoAlbum
from photo_album.serializers import PhotoSerializer, PhotoAlbumSerializer

PHOTO_URL = reverse('photo_album:photo-list')
PHOTO_ALBUM_URL = reverse('photo_album:album-list')


def sample_photo(user, title='Lovely Photo'):
    """
    create and return a sample photo without the image
    Image upload functionality is tested separately
    """
    return Photo.objects.create(user=user, title=title)


def sample_photo_album(user, **params):
    """
    create and return a sample photo album
    """
    defaults = {
        'title': 'Around the World',
    }
    defaults.update(params)
    album = PhotoAlbum.objects.create(user=user)
    album.photos.add(sample_photo(user))
    album.photos.add(sample_photo(user, title="Mount Everest"))


@pytest.mark.django_db
class TestPhotoAPIs:

    def test_auth_required(self, api_client):
        """test that auth is required"""
        res = api_client.get(PHOTO_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_photos(self, api_client, test_user):
        """test retrieving photos"""
        sample_photo(user=test_user)
        sample_photo(user=test_user, title="Dubai")

        api_client.force_authenticate(test_user)
        res = api_client.get(PHOTO_URL)

        photos = Photo.objects.all().order_by('-created')
        serializer = PhotoSerializer(photos, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_photos_limited_to_user(self, api_client, test_user):
        """test retrieving photos for user"""

        user2 = get_user_model().objects.create_user(
            'otheruser@company.com',
            'password123'
        )
        sample_photo(user=user2)
        sample_photo(user=test_user)

        api_client.force_authenticate(test_user)
        res = api_client.get(PHOTO_URL)

        photos = Photo.objects.filter(user=test_user)
        serializer = PhotoSerializer(photos, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data == serializer.data

    def test_create_photo(self, api_client, test_user):
        """test creating recipe with tags"""
        photo_1 = sample_photo(user=test_user, title='Home')

        payload = {
            'title': 'Home'
        }
        api_client.force_authenticate(test_user)
        res = api_client.post(PHOTO_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPhotoAlbumAPIs:

    def test_auth_required(self, api_client):
        """test that auth is required"""
        res = api_client.get(PHOTO_ALBUM_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_album(self, api_client, test_user):
        """test retrieving photo album"""

        sample_photo_album(user=test_user)
        sample_photo_album(user=test_user, title="2019")

        api_client.force_authenticate(test_user)
        res = api_client.get(PHOTO_ALBUM_URL)

        albums = PhotoAlbum.objects.all().order_by('-created')
        serializer = PhotoAlbumSerializer(albums, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_album_limited_to_user(self, api_client, test_user):
        """test retrieving photo album for user"""

        user2 = get_user_model().objects.create_user(
            'otheruser@company.com',
            'password123'
        )
        sample_photo_album(user=user2)
        sample_photo_album(user=test_user)

        api_client.force_authenticate(test_user)
        res = api_client.get(PHOTO_ALBUM_URL)

        albums = PhotoAlbum.objects.filter(user=test_user)
        serializer = PhotoAlbumSerializer(albums, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data == serializer.data

    def test_create_photo_album(self, api_client, test_user):
        """test creating recipe with tags"""
        photo_1 = sample_photo(user=test_user, title='Home')
        photo_2 = sample_photo(user=test_user, title='Work')

        payload = {
            'title': 'Holidays in LA',
            'photos': [str(photo_1.id), str(photo_2.id)],
        }

        api_client.force_authenticate(test_user)
        res = api_client.post(PHOTO_ALBUM_URL, payload)
        print(res.data)
        assert res.status_code == status.HTTP_201_CREATED
        album = PhotoAlbum.objects.get(id=res.data['id'])
        photos = album.photos.all()
        assert photos.count() == 2
