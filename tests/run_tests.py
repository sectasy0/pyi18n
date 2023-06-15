#!/usr/bin/env python3
# flake8: noqa
from os import path, mkdir, environ
from json import dumps
from yaml import dump
from pytest import main

from helpers import (test_path, locale_content,
                     bigger_files_path, bigger_locales,
                     empty_locales, corrupted_locales,
                     corrupted_path, corrupted_locales_yaml,
                     namespaced_content, namespaced_yml)


class ResultPlugin:
    """ Plugin for collecting test results
        This is due to that CI/CD tests won't fail
            if any test fails running via run_tests.py
    """
    def __init__(self):
        self.result = list()

    def pytest_runtest_logreport(self, report) -> None:
        """ called after test """
        self.result.append(report.outcome)

    def check_result(self) -> None:
        """ call exit(1) if any test fails """
        if 'failed' in self.result:
            exit(1)



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


def create_fixtures_namespaced() -> None:
    """ Create fixtures for namespaced """
    for locale in namespaced_content.items():
        locale_path: str = path.join(namespaced_yml, locale[0])
        if not path.exists(locale_path):
            mkdir(locale_path)

        for file, content in locale[1].items():

            with open(f"{locale_path}/{file}.json", "w", encoding="utf-8") as _f:
                _f.write(dumps(content, indent=4, sort_keys=False))

            with open(f"{locale_path}/{file}.yml", "w", encoding="utf-8") as _f:
                _f.write(dump(content, sort_keys=False))


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

    create_test_file('en', bigger_locales, bigger_files_path)

    create_corrupted_file()
    create_fixtures_namespaced()


if __name__ == "__main__":
    setup_fixtures()
    environ['PYI18N_TEST_ENV'] = '1'
    result: ResultPlugin = ResultPlugin()
    main(['-vv', '-s', '--log-cli-level=INFO'], plugins=[result])
    result.check_result()

