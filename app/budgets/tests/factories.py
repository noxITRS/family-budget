import factory

from budgets.models import Budget, BudgetCategory
from users.tests.factories import UserFactory


class BudgetCategoryFactory(factory.django.DjangoModelFactory):
    active = True

    class Meta:
        model = BudgetCategory


class BudgetFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("pystr", min_chars=1, max_chars=128)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Budget
