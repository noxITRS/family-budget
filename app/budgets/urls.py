from django.urls import path
from rest_framework.routers import DefaultRouter

from budgets.views import BudgetCategoryView, BudgetViewSet

app_name = "budgets"

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budgets")

urlpatterns = [
    path(r"budgets/categories", BudgetCategoryView.as_view(), name="categories"),
] + router.urls
