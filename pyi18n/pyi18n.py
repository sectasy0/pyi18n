from collections import defaultdict
from os import getcwd
from functools import reduce
from operator import getitem
from os.path import exists
from typing import Union

from .loaders import PyI18nBaseLoader

# TODO: figure out import error from tests/
try:
    from pyi18n.loaders import PyI18nYamlLoader
except ModuleNotFoundError:
    from loaders import PyI18nYamlLoader


class PyI18n:
    """ Main i18n localization class

    Attributes:
        available_locales (tuple): list of available locales
        load_path (str): path to locales directory
        _loaded_translations (dict): (class attribute) dictionary of loaded translations
    
    Methods:
        gettext(locale, path, **kwargs) -> Union[dict, str]
    
    Private Methods:
        __find (path, locale) -> Union[dict, str]
        __pyi18n_init () -> None

    Examples:
        >>> from pyi18n import PyI18n
        >>> pyi18n = PyI18n(["en", "jp"], "locales/")
        >>> pyi18n.gettext("en", "hello.world")
        'Hello, world!'
        >>> pyi18n.gettext("jp", "hello.world")
        'こんにちは、世界！'
    """

    _loaded_translations: dict = {}

    def __init__(self, 
            available_locales: tuple, 
            load_path: str = "locales/", 
            loader: PyI18nBaseLoader = None
        ) -> None:

        """ Initialize i18n class

        Args:
            available_locales (tuple): list of available locales
            load_path (str): path to locales directory

        Returns:
            None
        
        """

        self.available_locales: tuple = available_locales
        self.load_path: str = f"{getcwd()}/{load_path}"
        if loader is not None and loader.get_path() != self.load_path:
            self.load_path = loader.get_path()

        self.loader: PyI18nBaseLoader = loader or PyI18nYamlLoader(self.load_path)

        self.__pyi18n_init()

    def __pyi18n_init(self) -> None:
        """ validator and loader for translations

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: if locale is not available in self.available_locales
            FileNotFoundError: if translation file is not found

        """

        if not self.available_locales:
            raise ValueError("available locales must be specified")

        if not exists(self.load_path):
            raise FileNotFoundError(f"{self.load_path} directory not found, please create it")

        self._loaded_translations = self.loader.load(self.available_locales)


    def gettext(self, locale: str, path: str, **kwargs) -> Union[dict, str]:
        """ Get translation for given locale and path

        Args:
            locale (str): locale to get translation for
            path (str): path to translation
            **kwargs: interpolation variables

        Returns:
            Union[dict, str]: translation str, dict or error message

        Raises:
            ValueError: if locale is not in self.available_locales

        """

        if locale not in self.available_locales:
            raise ValueError(f"locale {locale} not specified in available locales")

        founded: Union[dict, str] = self.__find(path, locale)

        if len(kwargs) > 0 and isinstance(founded, str):
            try:
                return founded.format_map(defaultdict(str, **kwargs))
            except KeyError:
                return founded
            
        return founded
        
    def __find(self, path: str, locale: str) -> Union[dict, str]:
        """ Find translation for given path and locale
            
        Args:
            path (str): path to translation
            locale (str): locale to get translation for
        
        Returns:
            Union[dict, str]: translation str, dict or error message

        """
        try:
            return reduce(getitem, path.split('.'), 
                self._loaded_translations[locale])
        except (KeyError, TypeError):
            return f"missing translation for: {locale}.{path}"
    
    def get_loader(self) -> PyI18nBaseLoader:
        """ Return loader class

        Args:
            None

        Returns:
            PyI18nBaseLoader: loader class

        """
        return self.loader


if __name__ == "__main__":
    i18n = PyI18n(("en", "pl"), load_path="locales/")
    _ = i18n.gettext
    print(_("en", "hello", user="John"))