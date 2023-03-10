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
