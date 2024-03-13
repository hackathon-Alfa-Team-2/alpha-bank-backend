import pytest


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    """Подмена бекенда кеширования."""
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }


pytest_plugins = [
    "tests.pytest_tests.fixtures.users_fixtures",
    "tests.pytest_tests.fixtures.lms_fixtures",
]
