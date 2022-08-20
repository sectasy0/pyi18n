# flake8: noqa
import pytest
from pyi18n.tasks import normalize
from tests.helpers import test_path, empty_locales, not_raises


def test_should_normalize_locales():
    with not_raises(Exception):
        normalize.normalize_locales(test_path)


def test_normalize_invalid_locales_path():
    with pytest.raises(SystemExit):
        normalize.normalize_locales("some_invalid_path/")


def test_normalize_no_locale_in_locales():
    with pytest.raises(SystemExit):
        normalize.normalize_locales(empty_locales)
