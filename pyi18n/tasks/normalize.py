from os import listdir, getcwd
from os.path import exists
from typing import Any, Set, Dict
from xmltodict import unparse as xml_dump
from os import environ

# TODO: fix this ugly hack, problem with import during testing
try:
    import loaders
except ModuleNotFoundError:
    from pyi18n import loaders

from json import dump as json_dump
from yaml import dump as yaml_dump


def normalize_locales(locale_path: str = "locales/") -> dict:
    """ Sorts the keys in alphabetically order, and overrides files """

    # dir_content = listdir(locale_path)
    locale_path: str = f"{getcwd()}/{locale_path}"
    if not exists(locale_path):
        print(f"[ERROR] {locale_path} does not exist")
        exit(1)

    locales: Set = set([x.split('.')[0] for x in listdir(locale_path)])

    if not locales:
        print(f"[ERROR] {locale_path} is empty")
        exit(1)

    for subclass in loaders.PyI18nBaseLoader.__subclasses__():
        if subclass.__name__ == "PyI18nXMLLoader" \
         and environ["PYI18N_TEST_ENV"]:
            continue
        loader: loaders.PyI18nBaseLoader = subclass(locale_path)

        content: Dict[str] = loader.load(locales)

        sorted_content: Dict[Any] = __sort_nested(content)

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
    """ Sorts nested dictionaries """
    dictionary: dict = dictionary
    for d in dictionary:
        dictionary[d] = dict(sorted(dictionary[d].items()))
    return dict(dictionary)
