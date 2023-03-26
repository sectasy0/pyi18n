#!/usr/bin/env python3
# flake8: noqa
from os import path, mkdir, environ
from json import dumps
from yaml import dump
from pytest import main

from helpers import (test_path, locale_content,
                     bigger_files_path, bigger_locales,
                     empty_locales, corrupted_locales,
                     corrupted_path, corrupted_locales_yaml)


def create_corrupted_file() -> None:
    """ Create corrupted test file for locale. """

    if not path.exists(corrupted_path):
        mkdir(corrupted_path)

    with open(f"{corrupted_path}pl.json", "w", encoding="utf-8") as _f:
        _f.write(corrupted_locales)

    with open(f"{corrupted_path}pl.yml", "w", encoding="utf-8") as _f:
        _f.write(corrupted_locales_yaml)


def create_test_file(locale: str, content: dict, f_path: str) -> None:
    """ Create test file for locale. """
    with open(f"{f_path}{locale}.yml", "w", encoding="utf-8") as _f:
        _f.write(dump({locale: content}))
    with open(f"{f_path}{locale}.json", "w", encoding="utf-8") as _f:
        _f.write(dumps({locale: content}, indent=4))


def setup_fixtures() -> None:
    """ Setup fixture before running tests. """
    if not path.exists(test_path) \
       and not path.exists(bigger_files_path):

        mkdir(test_path)
        mkdir(bigger_files_path)

    if not path.exists(empty_locales):
        mkdir(empty_locales)

    for locale in locale_content.keys():
        with open(f"{test_path}/{locale}.yml", "w", encoding="utf-8") as _f:
            _f.write(dump({locale: locale_content[locale]}))
        with open(f"{test_path}/{locale}.json", "w", encoding="utf-8") as _f:
            _f.write(dumps({locale: locale_content[locale]}, indent=4))

        create_test_file(locale, locale_content[locale], test_path)

    create_test_file("en", bigger_locales, bigger_files_path)

    create_corrupted_file()


if __name__ == "__main__":
    setup_fixtures()
    environ['PYI18N_TEST_ENV'] = '1'
    main(['-vv', '-s'])
