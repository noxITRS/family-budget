from django.conf import settings
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(title="Family Budget", default_version="v1"),
    url=settings.API_URL,
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("users/", include("users.urls")),
    path("budgets/", include("budgets.urls")),
    # API Documentation
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
]
