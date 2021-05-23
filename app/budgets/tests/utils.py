from unittest.mock import ANY


def get_expected_budget_category(item, **kwargs):
    return {"slug": kwargs.get("slug", item.slug), "title": kwargs.get("title", item.title)}


def get_expected_budget(item, **kwargs):
    return {
        "created": ANY,
        "modified": ANY,
        "title": kwargs.get("title", item.title),
        "owner": kwargs.get("owner", item.owner_id),
        "operations_count": kwargs.get("operations_count", item.operations.count()),
    }
