"""
This module contains various helper functions and
utilities that can be used throughout the application.
"""

from os import listdir, stat
from os.path import exists, join, splitext
from typing import List
from yaml import FullLoader


def load_locale(path: str, ser_mod: object, l_type: str) -> dict:
    """Load translations from a single locale directory.

    Args:
        path (str): path to the locale directory
        ser_mod (object): module for serialization

    Return:
        dict: loaded translations for the locale
    """
    if not exists(path):
        print(f"[WARNING] path {path} doesn't exist, probably you forgot",
              "to add it to the available locales list.")
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

    return [file_name for file_name in listdir(path)
            if file_name.endswith(file_extension)]


def load_file(file_path: str, ser_mod: object, l_type: str) -> dict:
    """Load translations from a single file.

    Args:
        file_path (str): path to the translation file
        ser_mod (object): module for serialization
        l_type (str): type of file to load (e.g. "yaml", "json")

    Return:
        dict: loaded translations from the file
    """
    loader_params: dict = {'Loader': FullLoader} if l_type == 'yaml' else {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return ser_mod.load(file, **loader_params)
