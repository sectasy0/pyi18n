# PyI18n
> Simple and easy to use internationalization library inspired by Ruby i18n.

![Python version][python-image]

## Installation

```sh
pip install pyi18n-v2
```

## Using library in your application

A few motivating and useful examples of how pyi18n can be used.

In first step you have to create locales folder in your main application folder.
Then you can create your own locale files in this folder.

for example:

```sh
$ mkdir -p my_app/locales
$ touch my_app/locales/en.yml
$ touch my_app/locales/pl.yml
$ touch my_app/locales/de.yml
```

Then create an instance of `PyI18n` class. For custom locales directory you can pass it as an argument (default is in app_root/locale/).

```python
from pyi18n import PyI18n
# default load_path is locales/
# you can change this path by specifying load_path parameter
i18n = PyI18n(("en", "pl", "de", "jp"), load_path="translations/")
_ = i18n.gettext
print(_("en", "hello.hello_user", user="John"))
#> Hello John!
print(_("pl", "hello.hello_user", user="John"))
#> Witaj John!
print(_("de", "hello.hello_user", user="John"))
#> Hallo John!
print(_("jp", "hello.hello_user", user="John"))
#> こんにちは、ジョンさん！
```

## Creating custom loader class

To create custom locale loader you have to create a class which will inherit from PyI18nBaseLoader and override `load` method with all required parameters (see below). You can see an example of custom locale loader in `examples/custom_xml_loader.py`.

```python
from pyi18n.loaders import PyI18nBaseLoader

class MyCustomLoader(PyI18nBaseLoader):
    def load(self, locales: tuple, load_path: str):
        # load_path is the path where your loader will look for locales files
        # locales is a tuple of locales which will be loaded
        # return a dictionary with locale data
        return {}
```

Then pass your custom loader to PyI18n class.

```python
from pyi18n.loaders import PyI18nBaseLoader

class MyCustomLoader(PyI18nBaseLoader):
    def load(self, locales: tuple, load_path: str):
        # load_path is the path where your loader will look for locales files
        # locales is a tuple of locales which will be loaded

        ...your custom loader logic...

        # have to return a dictionary
        return {}

# don't use load_path in `PyI18n` constructor, if not using default yaml loader
if __name__ == "__main__":
    load_path = "locales/"
    loader = MyCustomLoader(load_path=load_path)
    i18n = PyI18n(("en",), loader=loader)
    _ = i18n.gettext
    print(_("en", "hello.hello_user", user="John"))
    #> Hello John!
```

## Run tests

```sh
python3 tests/run_tests.py
```

For any questions and suggestions or bugs please create an issue.

## Release History

* 1.0.0: Initial release

## Meta

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/sectasy0](https://github.com/sectasy0)

## Contributing

1. Fork it (<https://github.com/sectasy0/pyi18n>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`) 
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/python-3.6-blue
[pypi-image]: https://img.shields.io/badge/pypi-remly-blue
[pypi-url]:  pypi.org/project/pyi18n/