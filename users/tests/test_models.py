import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_new_superuser():
    db = get_user_model()
    super_user = db.objects.create_superuser(
        'testuser@super.com', 'password')
    assert super_user.email == 'testuser@super.com'
    assert super_user.is_superuser is True
    assert super_user.is_staff is True
    assert super_user.is_active is True
    assert str(super_user), "testuser@super.com"

    with pytest.raises(ValueError):
        db.objects.create_superuser(
            email='testuser@super.com',  password='password',
            is_superuser=False)

    with pytest.raises(ValueError):
        db.objects.create_superuser(
            email='testuser@super.com', password='password',
            is_staff=False)

    with pytest.raises(ValueError):
        db.objects.create_superuser(
            email='', password='password', is_superuser=True)


@pytest.mark.django_db
def test_new_user():
    db = get_user_model()
    user = db.objects.create_user(
        'testuser@user.com', 'password')
    assert user.email == 'testuser@user.com'
    assert user.is_superuser is False
    assert user.is_staff is False
    assert user.is_active is True

    with pytest.raises(ValueError):
        db.objects.create_user(
            email='', password='password')
