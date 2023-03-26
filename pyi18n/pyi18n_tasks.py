"""
PyI18n Command-line interface

This module provides a command-line interface for the normalize task,
    which sorts locales in alphabetical order.

Examples:
$ pyi18n-tasks normalize -p my_app/locales/
Sorts the locales in alphabetical order.
"""
from argparse import ArgumentParser
from .tasks import normalize


def cli() -> None:
    """ A command-line interface function """
    parser = ArgumentParser()
    parser.add_argument("normalize", help="Sort locales in alphabetical order")
    parser.add_argument("-p", "--path", help="Path to locales",
                        default="locales", type=str, required=False)

    args = parser.parse_args()
    if args.normalize:
        normalize.normalize_locales(args.path)
