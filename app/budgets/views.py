from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from budgets.models import Budget, BudgetCategory, BudgetOperation
from budgets.permissions import IsOwnerOrReadOnly
from budgets.serializers import (
    BudgetCategorySerializer,
    BudgetOperationSerializer,
    BudgetSerializer,
    BudgetShareSerializer,
)
from users.serializers import UserSerializer
from utils.viewsets import SerializerPerActionMixin

User = get_user_model()


class BudgetViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """
    API endpoint that allows users to view or edit budgets.
    """

    model = Budget
    queryset = Budget.objects
    serializer_class = BudgetSerializer
    serializer_classes = {"shared": UserSerializer}
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user) | Q(shared_to=self.request.user)).annotate(
            operations_count=Count("operations")
        )

    @swagger_auto_schema(method="get", request_body=None, responses={status.HTTP_200_OK: UserSerializer(many=True)})
    @swagger_auto_schema(
        methods=["post", "delete"],
        request_body=BudgetShareSerializer,
        responses={status.HTTP_200_OK: UserSerializer(many=True)},
    )
    @action(detail=True, methods=["get", "post", "delete"])
    def shared(self, request, **kwargs):
        budget = self.get_object()
        if request.method == "POST":
            self._add_shared_users(request, budget)
        elif request.method == "DELETE":
            self._delete_shared_users(request, budget)
        return Response(self.get_serializer_class()(budget.shared_to.all(), many=True).data)

    def _add_shared_users(self, request, budget):
        serializer = self._validate_share_serializer(request, budget)
        budget.shared_to.add(*serializer.validated_data["users"])

    def _delete_shared_users(self, request, budget):
        serializer = self._validate_share_serializer(request, budget)
        budget.shared_to.remove(*serializer.validated_data["users"])

    def _validate_share_serializer(self, request, budget):
        serializer = BudgetShareSerializer(data=request.data, context={"request": request, "budget": budget})
        serializer.is_valid(raise_exception=True)
        return serializer


class BudgetCategoryView(ListAPIView):
    model = BudgetCategory
    permission_classes = (AllowAny,)
    queryset = BudgetCategory.objects.active()
    serializer_class = BudgetCategorySerializer
