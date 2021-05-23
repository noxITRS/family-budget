from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.faker import Faker

User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    is_staff = False
    is_superuser = False
    is_active = True

    class Meta:
        model = User
