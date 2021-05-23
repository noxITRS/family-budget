import pytest
from django.conf import settings
from django.urls.exceptions import NoReverseMatch
from rest_framework.reverse import reverse


class TestURLs:
    def test_debug_render_panel(self):
        with pytest.raises(NoReverseMatch):
            reverse("djdt:render_panel")

    def test_debug_sql_explain(self):
        with pytest.raises(NoReverseMatch):
            reverse("djdt:sql_explain")

    def test_debug_sql_profile(self):
        with pytest.raises(NoReverseMatch):
            reverse("djdt:sql_profile")

    def test_debug_sql_select(self):
        with pytest.raises(NoReverseMatch):
            reverse("djdt:sql_select")

    def test_debug_template_source(self):
        with pytest.raises(NoReverseMatch):
            reverse("djdt:template_source")
