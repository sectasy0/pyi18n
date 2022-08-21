from os.path import exists
from xmltodict import parse
from pyi18n.loaders import PyI18nBaseLoader
from pyi18n import PyI18n


class PyI18nXMLLoader(PyI18nBaseLoader):
    """ Load translations for given locales using yaml

    Inherits from PyI18nBaseLoader

    Args:
        locales (tuple): locales to load

    Returns:
        dict: loaded translations
    """

    _type: str = "xml"

    def load(self, locales: tuple) -> dict:
        """ Load translations from xml files

        Args:
            locales (tuple): list of available locales
        Returns:
            dict: loaded translations

        """
        loaded: dict = {}
        for locale in locales:

            file_path: str = f"{self.load_path}{locale}.xml"
            if not exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as _f:
                loaded[locale] = parse(_f.read())[locale]

        return loaded


if __name__ == "__main__":
    loader: PyI18nXMLLoader = PyI18nXMLLoader("locales/")
    i18n: PyI18n = PyI18n(('en', 'pl'), loader=loader)
    print(i18n.gettext("en", "hello.world"))
    print(i18n.gettext("pl", "hello.world"))
    # >> Hello world!
    # >> Witaj świecie!
