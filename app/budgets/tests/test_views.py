import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from budgets.models import Budget, BudgetCategory
from budgets.tests.factories import BudgetCategoryFactory, BudgetFactory
from budgets.tests.utils import get_expected_budget, get_expected_budget_category
from users.tests.factories import UserFactory
from users.tests.utils import get_expected_user


@pytest.mark.django_db
class TestBudgetCategoryView:
    def setup(self):
        self.client = APIClient()
        self.endpoint = reverse("budgets:categories")

    def test_list_not_authenticated(self):
        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK

    def test_list_ordering(self):
        expected_results = [BudgetCategoryFactory(title="a"), BudgetCategoryFactory(title="b")]

        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [get_expected_budget_category(cat) for cat in expected_results]

    def test_list_not_active(self):
        cat = BudgetCategoryFactory(active=False)

        assert BudgetCategory.objects.count() == 1
        assert not BudgetCategory.objects.get(pk=cat.slug).active

        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


@pytest.mark.django_db
class TestBudgetViewSet:
    def setup(self):
        self.client = APIClient()

    def _authenticate_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        return user

    def test_list_not_authenticated(self):
        endpoint = reverse("budgets:budgets-list")
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}

    def test_list_own_budget(self):
        user = self._authenticate_user()
        budget = BudgetFactory(owner=user)
        endpoint = reverse("budgets:budgets-list")
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [get_expected_budget(budget)]

    def test_list_other_users_budget_not_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([])
        endpoint = reverse("budgets:budgets-list")
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_other_users_budget_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([user])
        endpoint = reverse("budgets:budgets-list")
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [get_expected_budget(budget)]

    def test_retrieve_not_authenticated(self):
        some_budget = BudgetFactory()
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": some_budget.id})
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}

    def test_retrieve_own_budget(self):
        user = self._authenticate_user()
        budget = BudgetFactory(owner=user)
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": budget.id})
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_expected_budget(budget)

    def test_retrieve_other_users_budget_not_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([])
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": budget.id})
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_other_users_budget_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([user])
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": budget.id})
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_expected_budget(budget)

    def test_create_not_authenticated(self):
        endpoint = reverse("budgets:budgets-list")
        response = self.client.post(endpoint, {"title": "Some Budget Title"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}

    def test_create_authenticated(self):
        user = self._authenticate_user()
        budget = BudgetFactory.build()  # build object but don't save in db
        endpoint = reverse("budgets:budgets-list")
        response = self.client.post(endpoint, {"title": budget.title})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == get_expected_budget(budget, owner=user.id)

    def test_delete_not_authenticated(self):
        some_budget = BudgetFactory()
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": some_budget.id})
        response = self.client.delete(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}

    def test_delete_other_users_budget_not_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([])
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": budget.id})
        response = self.client.delete(endpoint)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Budget.objects.filter(pk=budget.id).exists()

    def test_delete_other_users_budget_shared(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=other_user)
        budget.shared_to.set([user])
        endpoint = reverse("budgets:budgets-detail", kwargs={"pk": budget.id})
        response = self.client.delete(endpoint)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Budget.objects.filter(pk=budget.id).exists()

    def test_get_shared(self):
        user = self._authenticate_user()
        users = UserFactory.create_batch(2)
        budget = BudgetFactory(owner=user)
        budget.shared_to.set(users)

        endpoint = reverse("budgets:budgets-shared", kwargs={"pk": budget.id})
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [get_expected_user(user) for user in users]

    def test_post_shared_not_existing_user(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=user)

        endpoint = reverse("budgets:budgets-shared", kwargs={"pk": budget.id})

        response = self.client.post(endpoint, data={"users": ["not existing id"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_shared_one_user(self):
        user = self._authenticate_user()
        other_user = UserFactory()
        budget = BudgetFactory(owner=user)

        endpoint = reverse("budgets:budgets-shared", kwargs={"pk": budget.id})

        response = self.client.post(endpoint, data={"users": [other_user.id]})
        assert response.status_code == status.HTTP_200_OK
        assert budget.shared_to.count() == 1

    def test_post_shared_two_users(self):
        user = self._authenticate_user()
        users = [user.id for user in UserFactory.create_batch(2)]
        budget = BudgetFactory(owner=user)

        endpoint = reverse("budgets:budgets-shared", kwargs={"pk": budget.id})

        response = self.client.post(endpoint, data={"users": users})
        assert response.status_code == status.HTTP_200_OK
        assert budget.shared_to.count() == 2
