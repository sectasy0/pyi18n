import pytest

from pyi18n import PyI18n
from tests.helpers import test_path, locale_content

from pyi18n.loaders import PyI18nJsonLoader

def test_initialize_with_available_locales() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    assert i18n.available_locales == available_locales
    assert i18n._loaded_translations != {}
    assert i18n._loaded_translations["en"] != {}
    assert i18n._loaded_translations["pl"] != {}
    assert i18n.get_loader()._type == "yaml"

def test_initialize_with_custom_load_path() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    assert i18n.available_locales == available_locales
    assert i18n._loaded_translations != {}
    assert i18n._loaded_translations["en"] != {}
    assert i18n._loaded_translations["pl"] != {}
    assert i18n.get_loader()._type == "yaml"

def test_initialize_without_available_locales() -> None:
    with pytest.raises(ValueError):
        PyI18n(())

def test_initialize_with_invalid_load_path() -> None:
    available_locales: tuple = ("en", "pl")
    load_path: str = "some_invalid_path/"
    with pytest.raises(FileNotFoundError):
        i18n = PyI18n(available_locales, load_path=load_path)
        assert i18n._loaded_translations == {}

def test_initialize_with_non_existing_locale() -> None:
    available_locales: tuple = ("en", "pl", "ru")
    i18n = PyI18n(available_locales, load_path=test_path)
    assert i18n._loaded_translations.keys() != available_locales
    assert tuple(i18n._loaded_translations.keys()) == ("en", "pl")
    assert i18n.get_loader()._type == "yaml"

def test_gettext_without_locale() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    with pytest.raises(ValueError):
        i18n.gettext("", "hello.world")
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_invalid_locale() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    with pytest.raises(ValueError):
        i18n.gettext("ru", "hello.world")
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_invalid_path() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.world.invalid") for locale in available_locales] 
    assert translated == [
        "missing translation for: en.hello.world.invalid",
        "missing translation for: pl.hello.world.invalid"
    ]
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_valid_path() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.world") for locale in available_locales] 
    assert translated == ['Hello world!', 'Witaj świecie!']
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_interpolation() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.hello_user", user="John") for locale in available_locales] 
    assert translated == ['Hello John!', 'Witaj John!']
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_multiple_interpolation() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age", 
        name="John", surname="Conor", age=25) for locale in available_locales] 
    assert translated == [
        'Hello John Conor! You are 25 years old.', 
        'Witaj John Conor! Ty masz 25 lat.'
    ]
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_interpolation_and_missing_some_parameter() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age", 
        name="John") for locale in available_locales] 
    assert translated == [
        'Hello John ! You are  years old.', 
        'Witaj John ! Ty masz  lat.'
    ]
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_interpolation_and_missing_all_parameter() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age") for locale in available_locales] 
    assert translated == [
        'Hello {name} {surname}! You are {age} years old.', 
        'Witaj {name} {surname}! Ty masz {age} lat.'
    ]
    assert i18n.get_loader()._type == "yaml"

def test_gettext_with_interpolation_and_missing_all_parameter_and_missing_locale() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    with pytest.raises(ValueError):
        i18n.gettext("", "")
    assert i18n.get_loader()._type == "yaml"

def test_gettext_should_return_dict() -> None:
    available_locales: tuple = ("en", "pl")
    i18n = PyI18n(available_locales, load_path=test_path)
    translated = i18n.gettext("en", "hello")
    assert isinstance(translated, dict)
    assert translated == locale_content["en"]["hello"]
    assert i18n.get_loader()._type == "yaml"

def test_initialize_with_available_locales_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, load_path=test_path, loader=loader)
    assert i18n.available_locales == available_locales
    assert i18n._loaded_translations != {}
    assert i18n._loaded_translations["en"] != {}
    assert i18n._loaded_translations["pl"] != {}
    assert i18n.get_loader()._type == "json"

def test_initialize_with_custom_load_path_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, load_path=test_path, loader=loader)
    assert i18n.available_locales == available_locales
    assert i18n._loaded_translations != {}
    assert i18n._loaded_translations["en"] != {}
    assert i18n._loaded_translations["pl"] != {}
    assert i18n.get_loader()._type == "json"

def test_initialize_without_available_locales_json_loader() -> None:
    with pytest.raises(ValueError):
        PyI18n(())

def test_initialize_with_invalid_load_path_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    load_path: str = "some_invalid_path/"
    loader = PyI18nJsonLoader(load_path)
    with pytest.raises(FileNotFoundError):
        i18n = PyI18n(available_locales, loader=loader)
        assert i18n._loaded_translations == {}

def test_initialize_with_non_existing_locale_json_loader() -> None:
    available_locales: tuple = ("en", "pl", "ru")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    assert i18n._loaded_translations.keys() != available_locales
    assert tuple(i18n._loaded_translations.keys()) == ("en", "pl")
    assert i18n.get_loader()._type == "json"

def test_gettext_without_locale_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    with pytest.raises(ValueError):
        i18n.gettext("", "hello.world")
    assert i18n.get_loader()._type == "json"

def test_gettext_with_invalid_locale_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    with pytest.raises(ValueError):
        i18n.gettext("ru", "hello.world")
    assert i18n.get_loader()._type == "json"

def test_gettext_with_invalid_path_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.world.invalid") for locale in available_locales] 
    assert translated == [
        "missing translation for: en.hello.world.invalid",
        "missing translation for: pl.hello.world.invalid"
    ]
    assert i18n.get_loader()._type == "json"

def test_gettext_with_valid_path_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.world") for locale in available_locales] 
    assert translated == ['Hello world!', 'Witaj świecie!']
    assert i18n.get_loader()._type == "json"

def test_gettext_with_interpolation_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.hello_user", user="John") for locale in available_locales] 
    assert translated == ['Hello John!', 'Witaj John!']
    assert i18n.get_loader()._type == "json"

def test_gettext_with_multiple_interpolation_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age", 
        name="John", surname="Conor", age=25) for locale in available_locales] 
    assert translated == [
        'Hello John Conor! You are 25 years old.', 
        'Witaj John Conor! Ty masz 25 lat.'
    ]
    assert i18n.get_loader()._type == "json"

def test_gettext_with_interpolation_and_missing_some_parameter_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age", 
        name="John") for locale in available_locales] 
    assert translated == [
        'Hello John ! You are  years old.', 
        'Witaj John ! Ty masz  lat.'
    ]
    assert i18n.get_loader()._type == "json"

def test_gettext_with_interpolation_and_missing_all_parameter_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = [i18n.gettext(locale, "hello.hello_full_name_age") for locale in available_locales] 
    assert translated == [
        'Hello {name} {surname}! You are {age} years old.', 
        'Witaj {name} {surname}! Ty masz {age} lat.'
    ]
    assert i18n.get_loader()._type == "json"

def test_gettext_with_interpolation_and_missing_all_parameter_and_missing_locale_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    with pytest.raises(ValueError):
        i18n.gettext("", "")
    assert i18n.get_loader()._type == "json"

def test_gettext_should_return_dict_json_loader() -> None:
    available_locales: tuple = ("en", "pl")
    loader = PyI18nJsonLoader(test_path)
    i18n = PyI18n(available_locales, loader=loader)
    translated = i18n.gettext("en", "hello")
    assert isinstance(translated, dict)
    assert translated == locale_content["en"]["hello"]
    assert i18n.get_loader()._type == "json"