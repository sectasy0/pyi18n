""" This module contains functions for normalizing i18n localization files. """
from os import listdir, getcwd
from os.path import exists, isdir, join
from typing import Union, Dict
from pathlib import Path
from logging import error
import json
import yaml

from pyi18n import loaders


def normalize_locales(locale_path: str = 'locales/') -> Dict:
    """Sorts the keys in alphabetically order, and overrides files"""
    locale_path: str = f"{getcwd()}/{locale_path}"

    if not exists(locale_path):
        error(f"{locale_path} does not exist")
        exit(1)

    if is_directory_empty(locale_path):
        error(f"{locale_path} is empty")
        exit(1)

    __perform_normalize(locale_path)


def __perform_normalize(locale_path: str) -> None:
    """private method to perform normalization,
    should not be called directly"""

    namespaced: bool = are_locales_namespaced(locale_path)
    loader, ext = get_loader(locale_path, namespaced)
    locales: tuple = get_locales(locale_path, namespaced, ext)

    loader: loaders.PyI18nBaseLoader = loader(locale_path, namespaced)

    if not locales:
        error("no locales found, check your path")
        exit(1)

    __save_normalized(loader, locales, namespaced)


def __save_normalized(
    loader: loaders.PyI18nBaseLoader,
    locales: tuple,
    namespaced: bool = False,
) -> None:
    ext: str = loader.type.replace('yaml', 'yml')

    if not locales:
        error("no locales found, check your path")
        exit(1)

    translations: dict = loader.load(locales)

    serializers: dict = {
        "json": lambda c, f: json.dump(c, f, sort_keys=True, indent=4),
        "yml": yaml.dump,
    }

    ser_mod: type = serializers[ext]

    for locale in translations.items():
        if namespaced:
            namespace, content = locale

            for name, body in content.items():
                full_path: str = f"{loader.load_path}{namespace}/{name}.{ext}"
                file_override(body, full_path, ser_mod)

            return

        full_path: str = f"{loader.load_path}{locale[0]}.{ext}"
        file_override({locale[0]: locale[1]}, full_path, ser_mod)


def get_locales(locale_path: str, namespaced: bool, ext: str) -> tuple:
    """Returns a tuple of locales from the specified path.

    Args:
        locale_path (str): representing the path to the locales directory.
        namespaced (bool): tells function if should
                            look for loader in namespaced way.
        ext (str): A string representing the file extension of the locales.

    Return:
        tuple: locales found in the directory.
    """
    target_func: dict = {
        True: lambda: [p.name for p in Path(locale_path).iterdir() if p.is_dir()],
        False: lambda: [
            Path(file).stem for file in listdir(locale_path) if file.endswith(ext)
        ],
    }
    return tuple(target_func[namespaced]())


def file_override(content: dict, file_path: str, ser_mod: object) -> None:
    """Override the contents of the file at the specified file path.

    Args:
        content (dict): A dictionary representing the content to
                            be written to the file.
        file_path (str): A string representing the path to the file
                            to be overridden.
        ser_mod (object): An object representing the serialization module
                            to be used for writing.

    Return:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        ser_mod(content, file)


def are_locales_namespaced(locale_path: str) -> bool:
    """Check if locales are namespaced"""
    return all(
        map(
            lambda x: isdir(join(locale_path, x)), listdir(locale_path)
        )
    )


def get_loader(
    locale_path: str,
    namespaced: bool
) -> Union[loaders.PyI18nBaseLoader, str]:
    """Analyses given path and return loader based on that.
        Note you in your files you have to store only locales
        if you have other files not related to locales it could return
        false loader of even worse throw an exception

    Args:
        locale_path (str): locales path
        namespaced (bool): tells function if should
                            look for loader in namespaced way.

    Return:
        [loaders.PyI18nBaseLoader, str]

    """

    first: str = listdir(locale_path)[0]
    functions: dict[callable] = {
        True: lambda: listdir(join(locale_path, first))[0].split(".")[-1],
        False: lambda: first.split(".")[-1],
    }
    ext: str = functions[namespaced]()
    ext_loaders: dict[str] = {
        'yml': loaders.PyI18nYamlLoader,
        'json': loaders.PyI18nJsonLoader,
    }

    loader_class: Union[loaders.PyI18nBaseLoader, None] = ext_loaders.get(ext)

    if not loader_class:
        error(
            "You're not using default loader version, "
            "make sure you pass -l argument"
        )
        exit(1)

    return loader_class, ext


def is_directory_empty(directory_path: str) -> bool:
    """Check if given locale directory isn't empty"""
    return len(listdir(directory_path)) == 0
