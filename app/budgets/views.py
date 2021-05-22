from django.db.models import Count, Q
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from budgets.models import Budget, BudgetCategory, BudgetOperation
from budgets.serializers import BudgetCategorySerializer, BudgetOperationSerializer, BudgetSerializer
from utils.viewsets import SerializerPerActionMixin


class BudgetViewSet(
    SerializerPerActionMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that allows users to be viewed or edited.
    """

    model = Budget
    queryset = Budget.objects
    serializer_class = BudgetSerializer
    serializer_classes = {"operations": BudgetOperationSerializer}

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user) | Q(shared_to=self.request.user)).annotate(
            operations_count=Count("operations")
        )

    @action(detail=True, methods=["get"])
    def operations(self, request):
        budget = self.get_object()

        serializer = self.get_serializer(BudgetOperation.objects.filter(budget=budget))
        return Response(serializer.data)


class BudgetCategoryView(ListAPIView):
    model = BudgetCategory
    permission_classes = (AllowAny,)
    queryset = BudgetCategory.objects.active()
    serializer_class = BudgetCategorySerializer
