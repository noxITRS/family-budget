from rest_framework import serializers

from budgets.models import Budget, BudgetCategory, BudgetOperation


class BudgetSerializer(serializers.ModelSerializer):
    operations_count = serializers.IntegerField()

    class Meta:
        model = Budget
        fields = ("created", "modified", "owner", "operations_count")
        read_only_fields = ("created", "modified", "owner", "operations_count")


class BudgetOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetOperation
        fields = ("type", "budget", "category", "ammount")


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ("slug", "title")
        read_only_fields = ("slug", "title")
