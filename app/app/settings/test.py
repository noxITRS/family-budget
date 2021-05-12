from .base import *  # noqa pylint: disable=unused-wildcard-import
from .base import env

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY", default="test_django_secret_key")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}  # Does not cache
