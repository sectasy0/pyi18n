from os.path import exists
import yaml
import json

class PyI18nBaseLoader:
    """ PyI18n Base Loader class, supports yaml and json

    Attributes:
        load_path (str): path to translations
        _type (str): loader type
    
    Methods:
        load (tuple, object) -> dict: load translations for given locales and returns as python dict
        type () -> str: return loader type
        get_path () -> str: return loader path
    
    """

    _type: str = "base"

    def __init__(self, load_path: str = "locales/") -> None:
        """ Initialize loader class
                
        Args:
            load_path (str): path to translations
            
        Returns:
            None

        """
        self.load_path: str = load_path

    def load(self, locales: tuple, ser_mod: object) -> dict:
        """ Load translations for given locales
        
        Args:
            locales (tuple): locales to load
        
        Returns:
            dict: loaded translations

        Notes:
            Custom load function should be implemented in child classes and return python dict
        
        """

        file_extension: str = ser_mod.__name__.replace('yaml', 'yml')

        loaded: dict = {}
        for locale in locales:

            file_path: str = f"{self.load_path}{locale}.{file_extension}"
            if not exists(file_path):
                # raise FileNotFoundError(f"locale file not found: {file_path}")
                continue
            
            try:
                with open(file_path, 'r') as _f:
                    load_params: dict = {"Loader": yaml.FullLoader} if file_extension == "yml" else {}
                    loaded[locale] = ser_mod.load(_f, **load_params)[locale]
            except json.decoder.JSONDecodeError:
                continue
        return loaded

    def type(self) -> str:
        """ Return loader type
        
        Args:
            None
        
        Returns:
            str: loader type
        
        """
        return self.__class__._type

    def get_path(self) -> str:
        """ Return loader path
        
        Args:
            None
        
        Returns:
            str: loader path
        
        """
        return self.load_path


class PyI18nJsonLoader(PyI18nBaseLoader):

    _type: str = "json"

    def load(self, locales: tuple) -> dict:
        """ Load translations for given locales using json

        Inherits from PyI18nBaseLoader
        
        Args:
            locales (tuple): locales to load
        
        Returns:
            dict: loaded translations
        
        """

        return super().load(locales, json)


class PyI18nYamlLoader(PyI18nBaseLoader):

    _type: str = "yaml"
    
    def load(self, locales: tuple) -> dict:
        """ Load translations for given locales using yaml

        Inherits from PyI18nBaseLoader
        
        Args:
            locales (tuple): locales to load
        
        Returns:
            dict: loaded translations
        
        """

        return super().load(locales, yaml)