"""
This module defines the PyI18n loaders which
load translations from files in YAML or JSON format.
"""

from os.path import exists, join
from typing import Type
import json
import yaml

from pyi18n.helpers import load_locale


class LoaderType:
    """Enum for the different loader types."""

    BASE: str = "base"
    YAML: str = "yaml"
    JSON: str = "json"


class PyI18nBaseLoader:
    """PyI18n Base Loader class, supports yaml and json

    Attributes:
        load_path (str): path to translations
        namespaced (bool): tells loader should look for namespaces

        type (str): loader type
    """

    type: str = LoaderType.BASE

    def __init__(
        self,
        load_path: str = "locales/",
        namespaced: bool = False
    ) -> None:
        """Initialize loader class

        Args:
            load_path (str): path to translations
            namespaced (bool): namespaces support

        Return:
            None
        """
        self.load_path: str = load_path
        self.namespaced: bool = namespaced

    def load(self, locales: tuple, ser_mod: Type) -> dict:
        """Load translations for given locales,
            should be overridden in child classes.

        Args:
            locales (tuple): locales to load
            ser_mod (Type): serializer module

        Return:
            dict: loaded translations

        Notes:
            Custom load function should be implemented
            in child classes and return python dict
        """

        file_extension: str = ser_mod.__name__

        loaded: dict = {}
        for locale in locales:
            file_path: str = f"{self.load_path}{locale}.{file_extension}"

            if not exists(file_path):
                if file_extension == LoaderType.YAML and exists(f"{self.load_path}{locale}.yml"):
                    file_path = f"{self.load_path}{locale}.yml"
                else:
                    continue

            try:
                loaded[locale] = self.__load_file(
                    file_path, file_extension, ser_mod, locale
                )
            except (json.decoder.JSONDecodeError, yaml.YAMLError):
                continue

        return loaded

    def __load_file(
        self,
        file_path: str,
        ext: str,
        ser_mod: Type,
        locale: str
    ) -> dict:
        """loads content, should not be called directly

        Return:
            dict: loaded content
        """
        with open(file_path, "r", encoding="utf-8") as _f:
            load_params: dict = {
                "Loader": yaml.FullLoader} if ext in ("yml", "yaml") else {}

            return ser_mod.load(_f, **load_params)[locale]

    def _load_namespaced(self, locales: tuple, ser_mod: Type) -> dict:
        """Load translations from namespaces.

        Should be overridden in child classes.
        This will look for a locale (directories) and load all namespaces.

        Args:
            locales (tuple): locales to load
            ser_mod (Type): module for serialization

        Return:
            dict: loaded translations
        """
        loaded: dict = {}
        for locale in locales:
            path: str = join(self.load_path, locale)
            loaded_locale: dict = load_locale(path, ser_mod, self.type)

            if not loaded_locale:
                continue

            loaded.setdefault(locale, loaded_locale)

        return loaded

    def get_path(self) -> str:
        """Return loader path

        Return:
            str: loader path
        """
        return self.load_path


class PyI18nJsonLoader(PyI18nBaseLoader):
    """PyI18n JSON Loader class

    Attributes:
        load_path (str): path to translations
        namespaced (bool): tells loader should look for namespaces

        type (str): loader type
    """

    type: str = LoaderType.JSON

    def load(self, locales: tuple) -> dict:
        """Load translations for given locales using json

        Inherits from PyI18nBaseLoader

        Args:
            locales (tuple): locales to load

        Return:
            dict: loaded translations
        """

        if self.namespaced:
            return super()._load_namespaced(locales, json)

        return super().load(locales, json)


class PyI18nYamlLoader(PyI18nBaseLoader):
    """PyI18n YAML Loader class

    Attributes:
        load_path (str): path to translations
        namespaced (bool): tells loader should look for namespaces

        type (str): loader type
    """

    type: str = LoaderType.YAML

    def load(self, locales: tuple) -> dict:
        """Load translations for given locales using yaml

        Inherits from PyI18nBaseLoader

        Args:
            locales (tuple): locales to load

        Return:
            dict: loaded translations
        """
        if self.namespaced:
            return super()._load_namespaced(locales, yaml)

        return super().load(locales, yaml)
