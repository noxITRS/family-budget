from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from django.db import models
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField

from utils.models import TimeStampedModel, UUIDModel

User = get_user_model()


class Budget(UUIDModel, TimeStampedModel):
    title = models.CharField(max_length=128)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    shared_to = models.ManyToManyField(User, related_name="read_only_budgets", blank=True)


class BudgetCategoryManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class BudgetCategory(TimeStampedModel):
    slug = AutoSlugField(populate_from="title", primary_key=True, blank=True)
    title = models.CharField(max_length=32)
    active = models.BooleanField()

    objects = BudgetCategoryManager()

    class Meta:
        verbose_name_plural = "Budget categories"
        ordering = ("title",)


class BudgetOperation(UUIDModel, TimeStampedModel):
    INCOME = "IN"
    EXPENSE = "EX"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]

    type = models.CharField(max_length=2, choices=TYPE_CHOICES, editable=False)
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, related_name="operations")
    category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, related_name="operations")
    ammount = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")

    def clean(self):
        if self.type == self.INCOME and self.category and self.category.title != "Income":
            raise ValidationError(f'{self.type} cannot have different category then "Income".')

    def save(self, **kwargs):
        self.clean()
        return super().save(self, **kwargs)
