""" This module contains functions for normalizing i18n localization files. """
from os import listdir, getcwd
from os.path import exists
from os import environ
from json import dump as json_dump
from yaml import dump as yaml_dump
from xmltodict import unparse as xml_dump

# TODO: fix this ugly hack, problem with import during testing
try:
    import loaders
except ModuleNotFoundError:
    from pyi18n import loaders


def normalize_locales(locale_path: str = "locales/") -> dict:
    """ Sorts the keys in alphabetically order, and overrides files """

    locale_path: str = f"{getcwd()}/{locale_path}"
    if not exists(locale_path):
        print(f"[ERROR] {locale_path} does not exist")
        exit(1)

    locales: set = set([x.split('.')[0] for x in listdir(locale_path)])

    if not locales:
        print(f"[ERROR] {locale_path} is empty")
        exit(1)

    __perform_normalize(locales, locale_path)


def __perform_normalize(locales: set, locale_path: str) -> None:
    """ private method to perform normalization,
        should not be called directly"""

    for subclass in loaders.PyI18nBaseLoader.__subclasses__():
        if subclass.__name__ == "PyI18nXMLLoader" \
         and environ["PYI18N_TEST_ENV"]:
            continue

        loader: loaders.PyI18nBaseLoader = subclass(locale_path)
        content: dict = loader.load(locales)

        sorted_content: dict = __sort_nested(content)

        __save_normalized(locales, loader,
                          locale_path, sorted_content)


def __save_normalized(
                    locales: set,
                    loader: loaders.PyI18nBaseLoader,
                    locale_path: str,
                    sorted_content: dict
                    ) -> None:
    """ private function to save the normalized content,
        should not be called directly."""

    ext: str = loader.type().replace('yaml', 'yml')
    dumper: str = {
        "json": lambda x, y: json_dump(x, y, indent=4, sort_keys=True),
        "yml": yaml_dump,
        "xml": lambda x, _: xml_dump(x, pretty=True)
    }

    for locale in locales:
        file_path: str = f"{locale_path}{locale}.{ext}"
        with open(file_path, "w", encoding="utf-8") as _f:
            dumper[ext]({locale: sorted_content[locale]}, _f)


def __sort_nested(dictionary: dict) -> dict:
    """ private function to sort nested dictionaries """
    return {k: dict(sorted(v.items())) for k, v in dictionary.items()}
