from users.tests.utils import get_expected_user
from users.tests.factories import UserFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
import pytest
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


@pytest.mark.django_db
class TestUserViewSet:
    def setup(self):
        self.client = APIClient()
        self.endpoint = reverse("users:user-list")

    def test_list_not_authenticated(self):
        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}

    def test_list_average_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "You do not have permission to perform this action."}

    def test_list_staff_user(self):
        user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=user)
        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [get_expected_user(user) for user in User.objects.all()]

    def test_create(self):
        data = {"username": "string", "password": "string", "email": "user@example.com"}
        response = self.client.post(self.endpoint, data=data)
        data.pop("password")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(**data).exists()

    def test_create_the_same_user_twice(self):
        data = {"username": "string", "password": "string", "email": "user@example.com"}
        UserFactory(**data)
        assert User.objects.count() == 1

        response = self.client.post(self.endpoint, data=data)
        data.pop("password")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"username": ["A user with that username already exists."]}
        assert User.objects.filter(**data).count() == 1

    def test_me(self):
        endpoint = reverse("users:user-me")
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_expected_user(user)
