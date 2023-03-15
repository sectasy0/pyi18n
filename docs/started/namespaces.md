PyI18n supports namespaces, which allows you to organize your translations into separate groups.

To use PyI18n with namespaces, you need to define the loader object yourself. Here's an example:
```py
from pyi18n.loaders import PyI18nYamlLoader
from pyi18n import PyI18n

if __name__ == "__main__":
    loader: PyI18nYamlLoader = PyI18nYamlLoader('locales/', namespaced=True)
    pyi18n: PyI18n = PyI18n(('en_US', 'de_DE'), loader=loader)

```

In this example, we create an instance of the PyI18nYamlLoader class with the namespaced parameter set to True. This tells the loader to look for namespaced locales in separate folders instead of one single file for one locale.

Here's an example of the expected file structure for the locales:
```
locales
    en_US
        common.yml
        analysis.yml
    de_DE
        common.yml
        analysis.yml
```

To get a key that is located in the common namespace, you should use the dot notation in your translation call:
```py
_(locale, 'common.greetings')
```
