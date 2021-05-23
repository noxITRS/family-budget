import pytest
from django.core.exceptions import ValidationError
from djmoney.money import Money

from budgets.models import BudgetOperation
from budgets.tests.factories import BudgetCategoryFactory, BudgetFactory


@pytest.mark.django_db
class TestBudgetOperationModel:
    def test_save_income_category_income(self):
        cat = BudgetCategoryFactory(title="Income")
        operation = BudgetOperation(
            type=BudgetOperation.INCOME, budget=BudgetFactory(), category=cat, ammount=Money(10, "USD")
        )
        operation.save()

    def test_save_income_without_category(self):
        operation = BudgetOperation(
            type=BudgetOperation.INCOME, budget=BudgetFactory(), category=None, ammount=Money(10, "USD")
        )
        operation.save()

    def test_save_income_category_other_than_income(self):
        cat = BudgetCategoryFactory(title="Other than Income")
        operation = BudgetOperation(
            type=BudgetOperation.INCOME, budget=BudgetFactory(), category=cat, ammount=Money(10, "USD")
        )
        with pytest.raises(ValidationError):
            operation.save()
