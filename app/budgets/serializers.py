from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from budgets.models import Budget, BudgetCategory, BudgetOperation

User = get_user_model()


class BudgetSerializer(serializers.ModelSerializer):
    operations_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Budget
        fields = ("created", "modified", "title", "owner", "operations_count")
        read_only_fields = ("created", "modified", "owner", "operations_count")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret.get("operations_count"):
            ret["operations_count"] = 0
        return ret

    def save(self, **kwargs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            kwargs.update(owner=user)
        return super().save(**kwargs)


class BudgetShareSerializer(serializers.Serializer):
    user_id = PrimaryKeyRelatedField(many=True, queryset=User.objects.all())


class BudgetOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetOperation
        fields = ("type", "budget", "category", "ammount")


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ("slug", "title")
        read_only_fields = ("slug", "title")
