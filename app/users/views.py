from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserSerializer
from utils.viewsets import SerializerPerActionMixin

User = get_user_model()


class UserViewSet(SerializerPerActionMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_classes = {"create": UserCreateSerializer}

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        elif self.action in ["list", "retrieve", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action == "me":
            return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
