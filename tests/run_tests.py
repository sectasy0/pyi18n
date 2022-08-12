#!/usr/bin/env python3
from pytest import main
from yaml import dump
from os import path, mkdir
from json import dumps

from helpers import (test_path, locale_content, 
    bigger_files_path, bigger_locales)

def create_test_file(locale: str, content: dict, path: str) -> None:
    with open(f"{path}{locale}.yml", "w") as f:
        f.write(dump({locale: content}))
    with open(f"{path}{locale}.json", "w") as f:
        f.write(dumps({locale: content}, indent=4))


def setup_fixtures() -> None:

    if not path.exists(test_path) \
        and not path.exists(bigger_files_path):
        mkdir(test_path)
        mkdir(bigger_files_path)
    
    for locale in locale_content.keys():
        with open(f"{test_path}/{locale}.yml", "w") as f:
            f.write(dump({locale: locale_content[locale]}))
        with open(f"{test_path}/{locale}.json", "w") as f:
            f.write(dumps({locale: locale_content[locale]}, indent=4))

        create_test_file(locale, locale_content[locale], test_path)
    
    create_test_file("en", bigger_locales, bigger_files_path)


if __name__ == "__main__":
    setup_fixtures()
    args = ['-vv', '--tb=line']
    main(args)