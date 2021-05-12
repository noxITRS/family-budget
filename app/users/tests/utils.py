from unittest.mock import ANY


def get_expected_user(item, **kwargs):
    return {
        "id": kwargs.get("id", item.id),
        "username": kwargs.get("username", item.username),
        "email": kwargs.get("email", item.email),
        "date_joined": kwargs.get("date_joined", ANY),
    }
