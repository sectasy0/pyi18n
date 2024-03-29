### Version [1.2.2](https://pypi.org/project/pyi18n-v2/1.2.2/) - unreleased
* Fixes:
  * Downgrade PyYAML to >= 5.4, for compatibility with docker.
  * Make `normalize` task to work with namespaced locales.
* Others:
  *  Styles and formatting have been standardized.

### Version [1.2.1](https://pypi.org/project/pyi18n-v2/1.2.1/) - 26.03.2023

* Enhancements:
    * Remove ugly hack to make tests work due to incorrect imports.
    * Test coverage has been increased to 99%.

### Version [1.2.0](https://pypi.org/project/pyi18n-v2/1.2.0/) - 15.03.2023

* New Features:
    * Support for namespaces.

* Enhancements:
    * Implemented guidelines for integration with the Django framework.
    * Refactored the `tasks/normalize.py` `__sort_nested` method for improved efficiency.
    * Revised the `PyI18n` class constructor for better readability and maintainability.
    * Resolved `flake8` errors to ensure code adheres to the pep8 standard.

### Version [1.1.0](https://pypi.org/project/pyi18n-v2/1.1.0/) - 23.08.2022

* New Features:
    * Introduced the `normalize task` for improved organization.
    * Added the ability to run the `normalize task` through command-line interface.

### Version [1.0.0](https://pypi.org/project/pyi18n-v2/1.0.0/) - 2022-08-12

* Initial release.
