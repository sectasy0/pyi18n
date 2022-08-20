# flake8: noqa
import examples.custom_xml_loader

from tests.helpers import custom_loader_path


def test_custom_loader():
    loader = examples.custom_xml_loader.PyI18nXMLLoader(custom_loader_path)
    locales: tuple = ("en", "pl")
    loaded_locales = loader.load(locales)
    assert loaded_locales != {}
    assert tuple(loaded_locales.keys()) == locales
