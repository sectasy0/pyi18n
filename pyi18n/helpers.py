"""
This module contains various helper functions and
utilities that can be used throughout the application.
"""
from ast import Dict
from os.path import exists, join, splitext
from os import listdir, stat
from logging import warning
from typing import Any, List, Type
from pathlib import Path
from yaml import FullLoader


def load_locale(path: str, ser_mod: Type, l_type: str) -> dict:
    """Load translations from a single locale directory.

    Args:
        path (str): path to the locale directory
        ser_mod (object): module for serialization
        l_type (str): loader type

    Return:
        dict: loaded translations for the locale
    """
    if not exists(path):
        warning((
            f"path {path} doesn't exist, probably you forgot",
            "to add it to the available locales list.",
        ))
        return {}

    file_extension: str = ser_mod.__name__.replace('yaml', 'yml')

    loaded_locale: dict = {}
    for file_name in get_files(path, file_extension):
        file_path: str = join(path, file_name)
        namespace: str = splitext(file_name)[0]

        if not stat(file_path).st_size:
            continue

        locale_content = load_file(file_path, ser_mod, l_type)
        loaded_locale[namespace] = locale_content

    return loaded_locale


def get_files(path: str, file_extension: str) -> List[str]:
    """Get a list of files in a directory with a given file extension.

    Args:
        path (str): path to the directory
        file_extension (str): file extension to search for (e.g. ".yml")

    Return:
        List[str]: list of file names in the directory with the given extension
    """
    if not file_extension:
        return []

    return [
        fn for fn in listdir(path) if fn.endswith(file_extension)
    ]


def load_file(file_path: str, ser_mod: Type, l_type: str) -> Dict:
    """Load translations from a single file.

    Args:
        file_path (str): path to the translation file
        ser_mod (Callable): module for serialization
        l_type (str): type of file to load (e.g. "yaml", "json")

    Return:
        dict: loaded translations from the file
    """
    if not l_type:
        raise ValueError('l_type must be valid loader type')

    yaml_type: bool = l_type == 'yaml'
    loader_params: dict[str, Any] = {'Loader': FullLoader} if yaml_type else {}
    with open(file_path, "r", encoding="utf-8") as file:
        return ser_mod.load(file, **loader_params)


def get_locales(path: str, namespaced: bool, ext: str) -> tuple:
    """Returns a tuple of locales from the specified path.

    Args:
        path (str): A string representing the path to the locales directory.
        namespaced (bool): A boolean indicating the locales are namespaced.
        ext (str): A string representing the file extension of the locales.

    Return:
        tuple: A tuple of locales found in the directory.
    """
    target_func: dict = {
        True: lambda: [p.name for p in Path(path).iterdir() if p.is_dir()],
        False: lambda: [
            Path(file).stem for file in listdir(path) if file.endswith(ext)
        ],
    }
    return tuple(target_func[namespaced]())


def file_override(content: dict, file_path: str, ser_mod: Type) -> None:
    """Override the contents of the file at the specified file path.

    Args:
        content (dict): A dictionary representing the content.
        file_path (str): A string representing the path to the file.
        ser_mod (object): An object representing the serialization.

    Return:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        ser_mod.dump(content, file)
