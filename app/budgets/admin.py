from django.contrib import admin

from budgets.models import Budget, BudgetCategory, BudgetOperation


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass


@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "active")


@admin.register(BudgetOperation)
class BudgetOperationAdmin(admin.ModelAdmin):
    list_display = ("type", "budget", "category", "ammount")
    list_display_links = ("budget", "category")
