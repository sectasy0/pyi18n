# PyI18n
> PyI18n is a simple and easy to use internationalization library for Python, inspired by Ruby i18n.

![Python version][python-image] [![Code Climate](https://codeclimate.com/github/sectasy0/pyi18n/badges/gpa.svg)](https://codeclimate.com/github/sectasy0/pyi18n/coverage) [![Issue Count](https://codeclimate.com/github/sectasy0/pyi18n/badges/issue_count.svg)](https://codeclimate.com/github/sectasy0/pyi18n)

**Documentation available at [https://sectasy0.github.io/pyi18n](https://sectasy0.github.io/pyi18n).**

## Installation

You can install PyI18n via pip:
```sh
pip install pyi18n-v2
```

## Getting Started

A few motivating and useful examples of how pyi18n can be used.

To use PyI18n in your application, you will first need to create a locales folder in the root directory of your project. Within this folder, you can create locale files in the format of your choice (e.g. YAML, JSON).

For example:

```sh
$ mkdir -p my_app/locales
$ touch my_app/locales/en.yml
$ touch my_app/locales/pl.yml
$ touch my_app/locales/de.yml
```

You can then create an instance of the PyI18n class, passing in the desired languages and, optionally, a custom locales directory.

```python
from pyi18n import PyI18n

# default load_path is locales/
# you can change this path by specifying load_path parameter
i18n = PyI18n(("en", "pl", "de", "jp"), load_path="translations/")
_: callable = i18n.gettext

print(_("en", "hello.hello_user", user="John"))
#> Hello John!

print(_("pl", "hello.hello_user", user="John"))
#> Witaj John!

print(_("de", "hello.hello_user", user="John"))
#> Hallo John!

print(_("jp", "hello.hello_user", user="ジョンさん"))
#> こんにちは、ジョンさん！
```

## Namespaces

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

## Integrate pyi18n with Django project
To integrate pyi18n into your Django project, you will need to first add a locale field to your user model class. This field will store the user's preferred language, which will be used to retrieve the appropriate translations from the locales directory.

Next, you will need to configure pyi18n in your settings.py file by creating an instance of the PyI18n class and specifying the available languages. You can also create a gettext function for ease of use.

In your views, you can then use the gettext function to retrieve translations based on the user's preferred language. To use translations in templates, you will need to create a custom template tag that utilizes the gettext function.


### settings.py
```python
from pyi18n import PyI18n

i18n: PyI18n = PyI18n(['pl', 'en'])
_: callable = i18n.gettext
```

### views.py
```python
from mysite.settings import _

def index(request):
    translated: str = _(request.user.locale, 'hello', name="John")
    return HttpResponse(f"This is an example view. {translated}")
```

### register template tag
```python
from django import template
from mysite.settings import _

register = template.Library()

@register.simple_tag
def translate(locale: str, path: str, **kwargs):
    return _(locale, path, **kwargs)
```

### usage in templates
> **_NOTE:_**  Wrap this tag inside jinja2 special characters
```python
translate request.current_user.locale, "hello", name="John"
```

That's it, you have now successfully installed and configured PyI18n for your project. You can now use the provided gettext function to easily retrieve translations based on the user's preferred language. Additionally, you can use the provided template tag to easily retrieve translations in your templates. And if you need to use custom loaders you can use the PyI18nBaseLoader to create your own loaders.

---
## Creating custom loader class

To create custom locale loader you have to create a class which will inherit from PyI18nBaseLoader and override `load` method with all required parameters (see below). You can see an example of custom locale loader in `examples/custom_xml_loader.py`.

```python
from pyi18n.loaders import PyI18nBaseLoader


class MyCustomLoader(PyI18nBaseLoader):

    def load(self, locales: tuple, load_path: str):
        # load_path is the path where your loader will look for locales files
        # locales is a tuple of locales which will be loaded
        # return a dictionary with locale data

        ...your custom loader logic...

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
    load_path: str = "locales/"
    loader: PyI18nBaseLoader = MyCustomLoader(load_path=load_path)
    i18n: PyI18n = PyI18n(("en",), loader=loader)
    _: callable = i18n.gettext

    print(_("en", "hello.hello_user", user="John"))
    #> Hello John!
```

## Tasks

### Tasks usage

```sh
$ pyi18n-tasks
usage: pyi18n-tasks [-h] [-p PATH] normalize
pyi18n-tasks: error: the following arguments are required: normalize
```

### Normalization
Normalization process will sort locales alphabetically. The default normalization path is `locales/`, you can change it by passing `-p` argument.

```sh
$ pyi18n-tasks normalize
```

```sh
$ pyi18n-tasks normalize -p my_app/locales/
```

## Run tests

```sh
python3 tests/run_tests.py
```

For any questions and suggestions or bugs please create an issue.
## Limitations
* Normalization task will not work for custom loader classes except xml, cause it's based on loader type field ( If you have an idea how to solve this differently please open the issue with a description ), if you need that use one of build in loaders or user XML loader from example.

## Roadmap

See issues, If I have enough time and come up with a good idea on how this package can be improved, I'll post it there, along with tip.

## Release History

**Release History available at [https://sectasy0.github.io/pyi18n/home/release-history/](https://sectasy0.github.io/pyi18n/home/release-history/).**

## Contributing

1. Fork it (<https://github.com/sectasy0/pyi18n>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'feat: Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

[python-image]: https://img.shields.io/badge/python-3.6-blue
[pypi-image]: https://img.shields.io/badge/pypi-remly-blue
[pypi-url]:  pypi.org/project/pyi18n/
