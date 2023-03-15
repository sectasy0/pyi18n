"""
This module contains various helper functions and
utilities that can be used throughout the application.

Functions:
- load_locale: Load translations from a single locale directory.
"""

from os import listdir, stat
from os.path import exists, join, splitext
from yaml import FullLoader


def load_locale(path: str, ser_mod: object, l_type: str) -> dict:
    """Load translations from a single locale directory.

    Args:
        path (str): path to the locale directory
        ser_mod (object): module for serialization

    Returns:
        dict: loaded translations for the locale
    """
    if not exists(path):
        print("f[WARNING] path {path} doesn't exist, probably you forgot",
              "to add it to the available locales list.")
        return {}

    loader_params: object = {"Loader": FullLoader} if l_type == "yaml" else {}

    file_extension: str = ser_mod.__name__.replace('yaml', 'yml')

    loaded_locale: dict = {}
    for file_name in listdir(path):
        if not file_name.endswith(file_extension):
            continue

        file_path: str = join(path, file_name)
        namespace: str = splitext(file_name)[0]

        # Skip empty files
        if not stat(file_path).st_size:
            continue

        with open(file_path, 'r', encoding='utf-8') as file:
            locale_content: dict = ser_mod.load(file, **loader_params)

            loaded_locale[namespace] = locale_content

    return loaded_locale
