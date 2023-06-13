

Writing a custom loader with an example of a loader for XML file format.
To create your own loader, you have to inherit from `PyI18nBaseLoader` class and implement `load` method.

!!! note
    Your custom loader `load` method should return dictionary with translations otherwise your loader will not work.

```py
class PyI18nXMLLoader(PyI18nBaseLoader):

    type: str = "xml" # type of loader

    def load(self, locales: tuple) -> dict:
        # XML loader logic
        loaded: dict = {}
        for locale in locales:

            file_path: str = f"{self.load_path}{locale}.xml"
            if not exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as _f:
                loaded[locale] = parse(_f.read())[locale]

        return loaded
```

## Pass custom loader to PyI18n constructor

!!! tip
    Don't pass `load_path` argument to `PyI18n` constructor if you're using loader other than `PyI18nYamlLoader` (build-in). You should specify `load_path` argument in your loader instead.

```py
if __name__ == "__main__":
    loader: PyI18nXMLLoader = PyI18nXMLLoader("locales/")
    i18n: PyI18n = PyI18n(('en', 'pl'), loader=loader)
    print(i18n.gettext("en", "hello.world"))
    print(i18n.gettext("pl", "hello.world"))
    # >> Hello world!
    # >> Witaj świecie!

```
