from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    is_staff = False
    is_superuser = False
    is_active = True

    class Meta:
        model = User
