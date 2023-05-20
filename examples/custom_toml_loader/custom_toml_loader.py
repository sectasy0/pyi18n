from os.path import exists
from tomli import load
from pyi18n.loaders import PyI18nBaseLoader
from pyi18n import PyI18n


class PyI18nTOMLLoader(PyI18nBaseLoader):
    """ Load translations for given locales using toml

    Inherits from PyI18nBaseLoader

    Args:
        locales (tuple): locales to load

    Returns:
        dict: loaded translations
    """

    _type: str = "toml"

    def load(self, locales: tuple) -> dict:
        """ Load translations from toml files

        Args:
            locales (tuple): list of available locales
        Returns:
            dict: loaded translations

        """

        loaded: dict = {}
        for locale in locales:

            file_path: str = f"{self.load_path}{locale}.toml"
            if not exists(file_path):
                continue

            with open(file_path, "rb") as _f:
                loaded[locale] = load(_f)

        return loaded


if __name__ == "__main__":
    loader: PyI18nTOMLLoader = PyI18nTOMLLoader("locales/")
    i18n: PyI18n = PyI18n(('en', 'pl'), loader=loader)
    print(i18n.gettext("en", "hello.world"))
    print(i18n.gettext("pl", "hello.world"))
    # >> Hello world!
    # >> Witaj świecie!
